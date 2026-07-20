# JanAI — Dev Handoff Context

> **Purpose**: This file is a complete technical handoff for continuing development in a new chat session.  
> **Last updated**: March 5, 2026  

---

## 1. What Is JanAI

Voice-first AI platform for rural India. Users call a phone number (+1 831 298 8145), say their question in Hindi / Marathi / Tamil / English, and get a spoken AI answer. Also has a web frontend with a live browser call feature and a "call me back" widget.

**Hackathon project** — everything currently runs on a Twilio trial account (~$16 balance).

---

## 2. Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite 5 + Tailwind CSS 3 + React Router 6 |
| Browser Voice | `@twilio/voice-sdk` v2.18 (WebRTC) |
| Backend | AWS Lambda (Python 3.11) — single function `janai-call-handler` |
| API Gateway | REST — `https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod` |
| Database | AWS DynamoDB (3 tables + 1 new users table) |
| Storage | AWS S3 bucket `janai-documents` |
| LLM | Amazon Bedrock Nova Lite (primary) → OpenAI GPT-4o-mini (fallback if `OPENAI_API_KEY` set) |
| STT | Twilio native speech recognition (phone) |
| TTS | Sarvam AI bulbul:v2 → Amazon Polly fallback |
| Embeddings | AWS Bedrock Titan Embed v2 |
| Telephony | Twilio Voice |
| Auth | Custom JWT (PBKDF2 passwords, PyJWT, DynamoDB users table) |

---

## 3. Credentials (in `.env` at repo root)

> ⚠️ **Never commit real credentials.** Copy from the shared password manager / ask the project lead.
> All values below are placeholders — fill in from your `.env` file.

```
AWS_ACCESS_KEY_ID=<from .env / password manager>
AWS_SECRET_ACCESS_KEY=<from .env / password manager>
AWS_REGION=us-east-1

TWILIO_ACCOUNT_SID=<from .env / Twilio console>
TWILIO_AUTH_TOKEN=<from .env / Twilio console>
TWILIO_PHONE_NUMBER=+18312988145
TWILIO_API_KEY_SID=<from .env / Twilio console – API Keys>
TWILIO_API_KEY_SECRET=<from .env / Twilio console – API Keys>
TWILIO_TWIML_APP_SID=<from .env / Twilio console – TwiML Apps>

API_BASE_URL=https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod

SARVAM_API_KEY=<from .env / Sarvam dashboard>
OPENAI_API_KEY=<from .env / OpenAI dashboard>
LLM_PROVIDER=openai

BEDROCK_MODEL_ID=amazon.nova-micro-v1:0
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0

DYNAMODB_CALLS_TABLE=janai-calls
DYNAMODB_KNOWLEDGE_TABLE=janai-knowledge
DYNAMODB_VECTORS_TABLE=janai-vectors
DYNAMODB_USERS_TABLE=janai-users   ← needs to be created in DynamoDB console
S3_DOCUMENTS_BUCKET=janai-documents

JWT_SECRET=<pick a long random string, keep it secret>
```

---

## 4. Repository Structure

```
JanAI/
├── lambdas/
│   ├── call_handler/
│   │   ├── handler.py          ← MAIN backend (all routes)
│   │   └── connect_handler.py  ← Amazon Connect event handler
│   ├── call_initiator/
│   │   └── handler.py          ← standalone outbound call Lambda (not deployed—logic merged into call_handler)
│   └── websocket_handler/
│       └── handler.py          ← WebSocket handler (built but not deployed—not needed now)
├── website/
│   ├── src/
│   │   ├── App.jsx             ← Routes, AuthProvider wrapper
│   │   ├── context/
│   │   │   └── AuthContext.jsx ← JWT auth state, login/register/profile API calls
│   │   ├── pages/
│   │   │   ├── Home.jsx        ← Landing page, sticky CallMeBack widget, clickable scheme cards
│   │   │   ├── TryPage.jsx     ← Live Call (Twilio WebRTC) + Call Me Back tabs
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Profile.jsx     ← Edit profile + call history tabs
│   │   │   └── Pricing.jsx     ← Free/Pro/Business tiers
│   │   └── components/
│   │       └── layout/
│   │           └── Navbar.jsx  ← Auth-aware, mobile menu, Pricing link
│   ├── vercel.json             ← Vercel deployment config (SPA rewrites)
│   ├── .env.example            ← Frontend env var template
│   └── package.json
├── scripts/
│   ├── local_server.py         ← Flask dev server (port 8000) — proxies ALL Lambda routes
│   ├── deploy.py               ← Full AWS deploy script
│   └── seed_knowledge.py       ← Seeds DynamoDB knowledge/vectors tables
├── .env                        ← Real credentials (gitignored)
└── HANDOFF.md                  ← This file
```

---

## 5. All Backend API Routes (in `lambdas/call_handler/handler.py`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/voice/token` | Issues Twilio Access Token for browser WebRTC call |
| POST | `/voice/incoming` | Twilio webhook — new call arrives, plays welcome |
| POST | `/voice/language` | DTMF digit → sets language |
| POST | `/voice/gather` | Speech result → RAG → TTS → response |
| POST | `/call/initiate` | Web "Call Me Back" — creates outbound Twilio call |
| POST | `/chat` | Text chat REST endpoint (used by text mode) |
| POST | `/auth/register` | Create account (PBKDF2, DynamoDB) |
| POST | `/auth/login` | Returns JWT token |
| GET | `/profile` | Get profile (requires `Authorization: Bearer <token>`) |
| POST | `/profile` | Update profile fields |
| GET | `/profile/history` | Call history for the logged-in user |
| OPTIONS | * | CORS preflight |

---

## 6. Current Feature Status

### ✅ Working
- **Phone calls** — dial +1 831 298 8145, select language with DTMF, speak, get AI answer
- **Browser Live Call** — TryPage "Live Call" tab → Twilio WebRTC call via `@twilio/voice-sdk`
  - Language selection tabs before call, greeting skips DTMF menu
  - Mute button, live duration timer, animated pulse rings
- **Call Me Back** — enter phone number, Twilio places outbound call to user
  - Fixed: webhook URL was `localhost` before; now always uses production API Gateway URL
- **Text fallback** — type questions, get answers with TTS audio
- **Local dev server** (`scripts/local_server.py`) — Flask on port 8000, proxies all routes
- **RAG pipeline** — embeddings → cosine similarity → GPT-4o-mini → Sarvam TTS
- **User auth** (frontend + backend coded, but `janai-users` DynamoDB table not created yet)
- **Profile personalization** — if logged in, user profile injected into LLM system prompt
- **Phone caller lookup** — registered users recognized by phone, greeted by name
- **data.gov.in** — optional live scheme augmentation when `DATA_GOV_API_KEY` set
- **OG meta tags** — index.html has Twitter/OG tags
- **Vercel config** — `website/vercel.json` ready for deployment

### ⚠️ Built but NOT yet deployed to AWS
- `/chat`, `/call/initiate`, `/auth/*`, `/profile*`, `/voice/token` routes exist in handler.py but **API Gateway doesn't have these routes yet**
- The Lambda itself also needs redeployment with new env vars (`TWILIO_API_KEY_SID`, `TWILIO_API_KEY_SECRET`, `TWILIO_TWIML_APP_SID`, `DYNAMODB_USERS_TABLE`, `JWT_SECRET`, `API_BASE_URL`)
- `janai-users` DynamoDB table needs to be created (PK: `user_id`, type String)

### ❌ Not Done
- **Vercel deployment** — not deployed yet (config file is ready)
- **`janai-users` DynamoDB table** — not created in AWS console
- **Full AWS redeploy** — run `python scripts/deploy.py` to push all the new routes + new Lambda env vars

---

## 7. How to Run Locally

### Start backend (port 8000):
```bash
cd c:\Users\prakh\Documents\GitHub\JanAI
.\.venv\Scripts\python.exe scripts/local_server.py
```

### Start frontend (port 3001 if 3000 is busy):
```bash
cd website
npm run dev
```

Frontend will open at `http://localhost:3001`. It hits `http://localhost:8000` for API calls.

---

## 8. How to Deploy to AWS

Run once to push Lambda + create/update all API Gateway routes:
```bash
cd c:\Users\prakh\Documents\GitHub\JanAI
.\.venv\Scripts\python.exe scripts/deploy.py
```

This will:
1. Package `lambdas/call_handler/handler.py` + dependencies into a zip
2. Upload to S3 and update the `janai-call-handler` Lambda
3. Update Lambda env vars (all secrets from `.env`)
4. Create API Gateway routes for ALL new endpoints

**Before running**: Create the `janai-users` DynamoDB table manually:
- AWS console → DynamoDB → Create table
- Table name: `janai-users`
- Partition key: `user_id` (String)
- No sort key

---

## 9. How to Deploy Frontend to Vercel

```bash
cd website
npx vercel --prod
```

Set these env vars in the Vercel dashboard (Settings → Environment Variables):
```
VITE_API_BASE_URL = https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod
VITE_API_BASE     = https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod
VITE_TWILIO_PHONE = +18312988145
```

---

## 10. Key Implementation Notes

### Browser Voice Call Flow
1. User clicks big amber phone button on `/try` page
2. Frontend fetches `GET /voice/token?language=hi` from backend
3. Backend issues Twilio Access Token (API Key + TwiML App `AP9dd3...`)
4. `@twilio/voice-sdk` `Device.connect({ params: { lang: 'hi' } })` creates WebRTC call
5. Twilio calls the TwiML App webhook → `POST /voice/incoming?lang=hi` on API Gateway
6. Lambda detects `lang` param → skips DTMF menu → calls `_browser_call_welcome()`
7. Greets in chosen language → `<Gather>` for speech → `/voice/gather?lang=hi`
8. Speech → RAG (embeddings + DynamoDB knowledge base) → GPT-4o-mini → Sarvam TTS → plays back

### Call Me Back Flow
1. User submits phone number on `/try` → "Call Me Back" tab
2. Frontend POSTs to `/call/initiate` with `{ phone_number: "+91..." }`
3. Backend rate-limits (2 calls/hour), then calls `twilio_client.calls.create()`
4. Webhook URL is ALWAYS hardcoded to `API_BASE_URL` env var (production API Gateway) — never localhost
5. Twilio calls the user's phone and runs the same voice pipeline

### Auth System
- Passwords hashed with PBKDF2-HMAC-SHA256 (100k iterations)
- Tokens: PyJWT HS256, 7-day expiry, stored in `localStorage`
- If PyJWT not installed in Lambda, falls back to HMAC-signed JSON blob
- Profile fields: name, phone, language, occupation, state, district, enrolled_schemes, custom_context
- Profile injected into LLM prompt via `_build_profile_context()` → personalizes answers

### RAG Pipeline
- `get_embedding(query)` → Bedrock Titan Embed v2
- `retrieve_context(embedding, language)` → cosine similarity scan of `janai-vectors` table
- Returns top-3 chunks, language-prioritized (native lang text preferred)
- Optional: `_fetch_data_gov(query)` augments with live data.gov.in scheme data
- `ask_llm(query, context, language, history, profile_context)` → Amazon Bedrock Nova Lite

---

## 11. What To Work On Next

Priority order:

1. **Create `janai-users` DynamoDB table** (5 min, AWS console)
2. **Run `python scripts/deploy.py`** to push all backend changes to AWS Lambda + API Gateway
3. **Deploy frontend to Vercel** (`cd website && npx vercel --prod`)
4. **Test full end-to-end** — register account, log in, make browser call, verify personalization
5. **Polish**: loading states, error boundaries, mobile layout tweaks
6. **README update** with demo video / screenshots for hackathon submission
