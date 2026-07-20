# JanAI — Team Task Assignments
**Project:** JanAI |   
**Team:** Kaizen | Lead: jatin karma  
**Backend URL:** `https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod`  
**GitHub:** `https://github.com/jatin-karma/JanAI` (branch: `main`)

---

## PRODUCT CONTEXT (read before starting your task)

JanAI is a phone-first AI assistant for rural India. A user calls a number, selects their language (Hindi / Marathi / Tamil / English), and speaks naturally. The AI transcribes their speech (STT), retrieves verified knowledge (RAG), sends it to an LLM, and speaks the answer back (TTS) — in under 4 seconds.

**Core Stack:**
- **Backend:** AWS Lambda (`janai-call-handler`) behind API Gateway
- **LLM:** Amazon Bedrock (`amazon.nova-lite-v1:0`) via Converse API
- **TTS:** Sarvam AI `bulbul:v2` → Amazon Polly as fallback
- **STT:** Twilio's built-in speech recognition (for phone calls)
- **RAG:** DynamoDB tables: `janai-knowledge` (text), `janai-vectors` (embeddings via Amazon Titan)
- **Storage:** S3 bucket `janai-documents`
- **Auth:** JWT stored in DynamoDB `janai-users`

**AI Personality:** JanAI presents as a warm, caring didi (older sister). Always speaks in the user's chosen language. Female voice/grammar. Never robotic. Defined in `SYSTEM_PROMPT` inside `lambdas/call_handler/handler.py`.

---

---

# TASK FOR PRAKHYAT
## Web-Based Voice Testing Console + RAG Admin Portal

### Why This Matters
Right now, testing JanAI requires:
1. Making a real phone call (costs Twilio credits)
2. Speaking to a robot that may or may not respond

We need a **direct browser-based loop**: microphone → AWS Transcribe → Lambda LLM → Sarvam TTS → speaker. No Twilio. No phone. Completely on AWS free tier / credits. This also becomes the primary demo tool for judges.

Second, the AI is only as good as its knowledge. Right now the RAG database is thin. We need an admin portal where humans (and an AI agent) can view, add, edit, and verify entries. This is what keeps JanAI from hallucinating wrong phone numbers to someone in a crisis.

---

### TASK 1A — Web Voice Testing Console (STT → LLM → TTS in browser)

**Goal:** A standalone single-page app (can be added to `website/src/pages/`) where a developer/tester can:
1. Click a microphone button
2. Speak a question (in any of the 4 languages)
3. See the transcript appear in real time
4. See JanAI's response text appear
5. Hear JanAI's response played back via Sarvam TTS audio
6. See full conversation history (back and forth)
7. Select language (hi / mr / ta / en) from a dropdown

**Architecture to use (all AWS, no Twilio):**

```
Browser mic → Amazon Transcribe Streaming (WebSocket)
                        ↓
              POST /chat (existing Lambda endpoint)
                        ↓
              Sarvam TTS → audio URL → browser plays it
```

**Existing endpoint to hit:** `POST /chat`
```json
Request:  { "message": "pm kisan ke baare mein batao", "language": "hi", "session_id": "test-123" }
Response: { "response": "...", "audio_url": "..." }
```

**Amazon Transcribe Streaming Setup:**
- Use `amazon-transcribe` SDK or the WebSocket Streaming API directly
- You need temporary AWS credentials in the browser. Options:
  - Option A (easier): Add a `/voice/transcribe-token` Lambda endpoint that returns STS temporary credentials scoped to `transcribe:StartStreamTranscription` only
  - Option B (more work but better): Proxy the audio through a small Lambda websocket handler
- Language mapping: hi-IN, mr-IN, ta-IN, en-IN

**Frontend stack:** React (already used in `website/src/`). Create `website/src/pages/DevConsolePage.jsx`. Add route `/dev` in the router (inside `website/src/App.jsx`). Do NOT put this page in the main nav — it's a dev tool.

**What NOT to do:** Don't use the browser's built-in `webkitSpeechRecognition` — it won't work reliably in production and doesn't match what Twilio uses.

**Files to look at:**
- `website/src/pages/TryPage.jsx` — existing Try page for UI patterns
- `lambdas/call_handler/handler.py` lines ~408–435 — the `/chat` endpoint handler
- `website/src/App.jsx` — where to add the route
- `website/.env` — add `VITE_API_BASE_URL` is already there

---

### TASK 1B — RAG Admin Portal

**Goal:** A password-protected web page (or separate subdirectory) where an admin can:
1. **View** all entries in `janai-knowledge` DynamoDB table
2. **Add** new entries (form with: title, text_hi, text_mr, text_ta, text_en, category, source_url, helplines)
3. **Edit** existing entries
4. **Delete** entries
5. **Verify/Approve** entries (set `verified: true`, record who approved it)
6. **Trigger AI review** — a button that sends an entry to Bedrock Claude to fact-check it and returns a PASS / FLAG / FAIL + reason
7. **Search** entries by category or keyword

**Backend — new Lambda endpoints to add in `handler.py`:**
```
GET  /admin/rag               → list all entries (paginated)
POST /admin/rag               → create new entry (auto-generates embedding via Titan)
PUT  /admin/rag/{id}          → update entry
DELETE /admin/rag/{id}        → delete entry
POST /admin/rag/{id}/verify   → mark as verified
POST /admin/rag/{id}/ai-review → run Bedrock review agent on this entry
```

All `/admin/` routes must check for `Authorization: Bearer <admin_jwt>` header. Use the existing JWT logic in handler.py. Add an `is_admin: true` flag on the user record in DynamoDB.

**DynamoDB `janai-knowledge` entry schema (already exists, extend it):**
```python
{
  "id": "uuid",
  "category": "healthcare | agriculture | legal | finance | education | emergency | general",
  "title": "PM-Kisan Samman Nidhi",
  "text_hi": "...",    # Hindi
  "text_mr": "...",    # Marathi
  "text_ta": "...",    # Tamil
  "text_en": "...",    # English
  "helpline_numbers": ["155261"],   # NEVER let LLM generate these — always from DB
  "source_url": "https://pmkisan.gov.in",
  "documents_required": ["Aadhaar", "Land record"],
  "verified": False,
  "verified_by": None,
  "verified_at": None,
  "ai_review_status": None,   # "PASS" | "FLAG" | "FAIL"
  "ai_review_notes": None,
  "created_at": 1772723150,
  "updated_at": 1772723150,
}
```

**The AI Review Agent (Bedrock):**
When an admin clicks "AI Review" on an entry, the Lambda should:
1. Pull the entry's text_hi and text_en
2. Send to Bedrock Converse API with this system prompt:
```
You are a fact-checking agent for JanAI, a voice AI for rural India.
Review this knowledge base entry and check:
1. Are phone numbers real and currently active Indian government numbers?
2. Are eligibility criteria consistent with official govt website text?
3. Are benefit amounts correct (cross-check your training data)?
4. Is any information potentially harmful or dangerously wrong?
Return JSON: {"status": "PASS" | "FLAG" | "FAIL", "issues": [...], "confidence": 0-1}
```
3. Store the result back on the entry
4. Return it to the frontend

**Frontend (`website/src/pages/AdminPage.jsx`):**
- Simple table view of all entries
- Filter by category / verified status
- Click a row to open edit form (all 4 language text fields, side by side)
- "AI Review" button per row → shows spinner → shows result badge (green/yellow/red)
- Protected by login (use existing `/auth/login` endpoint, store JWT in localStorage under key `janai_admin_token`)

---

### TASK 1C — RAG Data Expansion (Claude Agent Task)

Use Claude (or any AI coding agent you have access to) to generate seed data for the following categories. Each entry must have text in all 4 languages (hi, mr, ta, en).

**Priority categories to fill (these are the things JanAI CANNOT get wrong):**

1. **Emergency Helplines** (highest priority)
   - Police: 100, Women helpline: 1091, Ambulance: 108, Fire: 101, Child helpline: 1098, PM-KISAN: 155261, Kisan Call Centre: 1800-180-1551, Mental health: iCall 9152987821, Vandrevala 1860-2662-345

2. **Government Schemes** (10 most important)
   - PM-KISAN, PM Awas Yojana, Ayushman Bharat, PM Jan Dhan, Sukanya Samriddhi, PM Mudra, MGNREGA, Ration Card / PDS, Beti Bachao Beti Padhao, NSP Scholarships

3. **Medical Emergencies** — What to do in first 10 minutes for: heart attack, snake bite, severe burns, choking, unconscious person, high fever in child, severe allergic reaction

4. **Legal Rights** — Rights of domestic violence victims, rights when arrested, rights of a farmer in case of crop failure (PMFBY), right to free legal aid, how to file RTI

5. **Agriculture** — MSP rates for top 10 crops (Kharif + Rabi), PM Fasal Bima Yojana claim process, KCC (Kisan Credit Card) how to apply

**Format for each entry (Python dict, paste into `scripts/seed_knowledge.py` or the admin portal):**
```python
{
  "category": "emergency",
  "title": "National Emergency Helplines",
  "text_hi": "भारत में आपातकालीन नंबर: पुलिस 100, एम्बुलेंस 108...",
  "text_mr": "...",
  "text_ta": "...",
  "text_en": "...",
  "helpline_numbers": ["100", "108", "112"],
  "source_url": "https://www.india.gov.in/topics/administration/emergency-helpline",
  "verified": False
}
```

**How to seed:** Once admin portal is up, use it. Or run `scripts/seed_knowledge.py` which already has the logic to embed and store entries. Check that file for the `add_entry()` function.

---

---

# TASK FOR SOMYA
## AWS Console Setup Check + RAG Strategy Review + Twilio / Call Flow Ownership

---

### FIRST: How to Access the AWS Console

1. Go to **https://console.aws.amazon.com**
2. Sign in with the team AWS account credentials (get from jatin)
3. **IMPORTANT — always set region to `us-east-1` (US East N. Virginia)** — top-right dropdown. If you're in the wrong region, you'll see empty tables and think nothing exists.

---

### Task 2A — Verify AWS Resources Are Set Up Correctly

#### Step 1 — Check DynamoDB Tables

Go to: **AWS Console → DynamoDB → Tables** (make sure region = us-east-1)

You should see exactly these 4 tables:

| Table Name | Key(s) | Expected Items |
|---|---|---|
| `janai-calls` | `call_id` (hash) + `timestamp` (range) | 40+ |
| `janai-knowledge` | `scheme_id` (hash) + `section_id` (range) | 64 entries |
| `janai-vectors` | `embedding_id` (hash) | 192 entries |
| `janai-users` | `user_id` (hash) | 0 (empty, freshly created) |

> **Note:** `janai-users` was missing and has just been created by jatin. If you still don't see it, wait 1–2 minutes and refresh — DynamoDB takes a moment to provision.

If any table is missing, run this command (you'll need AWS CLI installed — see below):
```powershell
# Check all tables
aws dynamodb list-tables --region us-east-1

# Create janai-users if missing:
aws dynamodb create-table `
  --table-name janai-users `
  --attribute-definitions AttributeName=user_id,AttributeType=S `
  --key-schema AttributeName=user_id,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --region us-east-1

# Create janai-knowledge if missing:
aws dynamodb create-table `
  --table-name janai-knowledge `
  --attribute-definitions AttributeName=scheme_id,AttributeType=S AttributeName=section_id,AttributeType=S `
  --key-schema AttributeName=scheme_id,KeyType=HASH AttributeName=section_id,KeyType=RANGE `
  --billing-mode PAY_PER_REQUEST `
  --region us-east-1

# Create janai-vectors if missing:
aws dynamodb create-table `
  --table-name janai-vectors `
  --attribute-definitions AttributeName=embedding_id,AttributeType=S `
  --key-schema AttributeName=embedding_id,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --region us-east-1

# Create janai-calls if missing:
aws dynamodb create-table `
  --table-name janai-calls `
  --attribute-definitions AttributeName=call_id,AttributeType=S AttributeName=timestamp,AttributeType=N `
  --key-schema AttributeName=call_id,KeyType=HASH AttributeName=timestamp,KeyType=RANGE `
  --billing-mode PAY_PER_REQUEST `
  --region us-east-1
```

#### Step 2 — Check the Lambda Function

Go to: **AWS Console → Lambda → Functions**

You should see: `janai-call-handler`

Click it → **Configuration → Environment variables** → verify these are present:

| Variable | Expected Value |
|---|---|
| `DYNAMODB_CALLS_TABLE` | `janai-calls` |
| `DYNAMODB_KNOWLEDGE_TABLE` | `janai-knowledge` |
| `DYNAMODB_VECTORS_TABLE` | `janai-vectors` |
| `DYNAMODB_USERS_TABLE` | `janai-users` |
| `S3_DOCUMENTS_BUCKET` | `janai-documents` |
| `BEDROCK_MODEL_ID` | `amazon.nova-lite-v1:0` |
| `BEDROCK_EMBEDDING_MODEL_ID` | `amazon.titan-embed-text-v2:0` |
| `TWILIO_ACCOUNT_SID` | `[REDACTED]` |
| `TWILIO_AUTH_TOKEN` | `[REDACTED]` |
| `TWILIO_PHONE_NUMBER` | `+18312988145` |
| `API_BASE_URL` | `https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod` |
| `LLM_PROVIDER` | `bedrock` |

If any are missing, go to **Configuration → Environment variables → Edit** and add them.

#### Step 3 — Check the S3 Bucket

Go to: **AWS Console → S3**

You should see bucket: `janai-documents`

Inside it, check for folder `static-audio/` which should contain:
- `welcome_intro.wav`
- `welcome_hi.wav`
- `welcome_mr.wav`
- `welcome_ta.wav`
- `welcome_en.wav`
- `no_input.wav`

If that folder is empty or missing, tell jatin — those audio files need to be regenerated.

#### Step 4 — Install AWS CLI (if you don't have it)

On Windows, download from: https://aws.amazon.com/cli/  
After install, configure with:
```powershell
# Get credentials from .env file or jatin
aws configure
# AWS Access Key ID: [REDACTED]
# AWS Secret Access Key: [REDACTED]
# Default region: us-east-1
# Default output format: json
```

Test it works:
```powershell
aws dynamodb list-tables --region us-east-1
# Should print: janai-calls, janai-knowledge, janai-vectors, janai-users
```

#### Step 5 — Check CloudWatch Logs (for debugging)

When a call fails or something breaks, go to:
**AWS Console → CloudWatch → Log groups → `/aws/lambda/janai-call-handler`**

Click the latest log stream → look for lines starting with `[ERROR]`. This tells you exactly what went wrong.

Or via CLI (last 5 minutes of errors):
```powershell
aws logs filter-log-events `
  --log-group-name "/aws/lambda/janai-call-handler" `
  --start-time ([DateTimeOffset]::UtcNow.AddMinutes(-5).ToUnixTimeMilliseconds()) `
  --region us-east-1 `
  --query "events[*].message" --output text | Select-String "ERROR"
```

---

### Is the RAG implementation correct?

**Short answer: Yes, the architecture is correct — but the database is nearly empty.**

The current approach:
1. User's speech transcript → embed with Titan → cosine similarity search in `janai-vectors`
2. Top 3 matching knowledge entries → injected into LLM context
3. LLM generates response using injected context + system prompt
4. Critical fields (helpline numbers) are appended AFTER LLM response from DB directly (LLM never generates these)

This is the right pattern. The problem is the knowledge base currently has only a handful of scheme entries. The AI falls back to raw LLM knowledge (Amazon Nova Lite) when RAG finds nothing useful — and Nova Lite does not reliably know Indian government scheme details.

**Your RAG tasks:**

#### Task 2A — Audit the current RAG data
Go to the `janai-knowledge` DynamoDB table (AWS Console → DynamoDB → Tables → janai-knowledge → Explore items). Check:
- How many entries exist?
- Are they in all 4 languages?
- Do they have embeddings (check `janai-vectors` table for matching IDs)?

Run the seed script to check what's in there:
```
cd c:\Users\makew\OneDrive\Desktop\Projects\JanAI
.venv\Scripts\activate
python scripts/seed_knowledge.py
```

#### Task 2B — Phone call flow ownership
You own the Twilio call experience. Current flow:

```
Incoming call → /voice/incoming (plays 5 welcome audio clips in 4 languages)
User presses 1/2/3/4 → /voice/language (sets language)
User speaks → Twilio Gather STT → /voice/gather (sends to RAG+LLM, plays TTS response)
```

Issues to fix:
1. **No-input timeout** — if user says nothing for 5 seconds, it plays `no_input.wav` and asks again. Verify this is working.
2. **Long responses** — Sarvam TTS generates one audio file per response. If response is > 300 tokens, the TTS URL may expire before Twilio can stream it. Add a check: if `len(response) > 800 chars`, truncate or split.
3. **Fallback language** — if Twilio STT sends back empty speech for a language, fall back to asking the user to repeat (currently it crashes silently).

Look at `lambdas/call_handler/handler.py` → `handle_gather()` function (around line 150–200).

#### Task 2C — Update the caller disclaimer text on the website
In `website/src/pages/TryPage.jsx`, near the bottom there's a yellow disclaimer box that says:
> "our system will call you from a US number (+1 260 204 8966)"

Change `+1 260 204 8966` to `+1 831 298 8145` (that's the real Twilio number now).

---

---

# TASK FOR PRATEEK
## Content, Quality Assurance, and Claude-Powered Data Generation

### Your Role
You don't need to write code. Your job is to use Claude (or any strong AI agent) to generate high-quality, accurate content for JanAI's brain, and to test the system from a user's perspective. Think of yourself as the Quality Officer — you decide what goes into the AI's knowledge base and whether the answers it gives are acceptable.

---

### Task 3A — Generate RAG Knowledge Entries Using Claude

Open Claude (claude.ai) and run the following prompt template for each category. Copy the output and share it with divya to load into the admin portal.

**Claude Prompt Template:**
```
You are helping build JanAI, a voice AI assistant for rural India that helps people access government services and critical information.

Generate 5 knowledge base entries for the category: [CATEGORY NAME]

Each entry must be in this exact JSON format:
{
  "category": "[category]",
  "title": "...",
  "text_hi": "... (natural Hindi, 2-3 sentences, conversational, as spoken on phone)",
  "text_mr": "... (natural Marathi, not just Google Translate)",
  "text_ta": "... (natural Tamil)",
  "text_en": "... (simple English, class 6 reading level)",
  "helpline_numbers": ["..."],   // only real, verified Indian numbers
  "source_url": "...",           // official govt URL for verification
  "documents_required": ["..."] // only if applicable
}

Categories to generate entries for (run separately):
1. emergency_helplines
2. agriculture_schemes
3. healthcare
4. legal_rights
5. education_scholarships
6. women_safety
7. child_welfare
8. senior_citizen_benefits

Important rules:
- Phone numbers MUST be real Indian government helpline numbers
- Amounts (like PM-KISAN ₹6000/year) must be currently accurate
- Language must be conversational, not bureaucratic
- A rural woman with class 5 education should understand the Hindi text when spoken aloud
```

Run this for each of the 8 categories. Verify the phone numbers by Googling them before sharing.

---

### Task 3B — Test JanAI as a Real User

Call `+18312988145` (JanAI's Twilio number). Test these scenarios and write a short note on what worked and what didn't:

| # | Scenario | Expected Behaviour |
|---|---|---|
| 1 | Call and press 1 (Hindi) | Welcome + hear "कोई सवाल पूछिए" |
| 2 | Ask "PM Kisan kya hai" | Accurate answer + helpline 155261 |
| 3 | Ask "mujhe paise nahi mil rahe khet mein" | Empathetic, asks for details, suggests PMFBY/Kisan CC |
| 4 | Call and press 3 (Tamil) | Responds in Tamil |
| 5 | Don't say anything | Should repeat the prompt, not crash |
| 6 | Ask "mera paisa kab aayega" (vague) | Should ask clarifying question, not hallucinate |
| 7 | Ask a healthcare question ("bukhar ke liye kya karoon") | Suggests home care + 108 for emergency |

Document each outcome and share with jatin.

---

### Task 3C — QA the Website

Visit `http://localhost:3000` (or the Vercel URL once deployed) and check:

1. Does "Call Me Back" work with your phone number?
2. Is the disclaimer text showing the right phone number (+1 831 298 8145)?
3. Does the mascot (AI avatar) appear? Does she animate?
4. Try the chat on the website — does JanAI answer correctly?
5. Try registering an account and logging in — does it work?
6. On mobile (use browser DevTools or your phone) — does the layout look right?

Write a simple bug list: **[Page] → [What's broken] → [Screenshot if possible]**

---

### Task 3D — Write the Demo Script (for hackathon judges)

Write a 3-minute demo script that jatin can follow during the presentation. Structure:
1. **(30 sec)** Problem: "Imagine you're a farmer in Vidarbha, no smartphone, only a ₹800 phone..."
2. **(60 sec)** Live Call Demo: Call the number, select Hindi, ask about PM-KISAN
3. **(30 sec)** Show the website — Call Me Back feature, the AI mascot
4. **(30 sec)** Show the architecture slide — "All on AWS, under $2 per 1000 calls"
5. **(30 sec)** Impact numbers: 500M potential users, 4 languages, 24/7, no app needed

---

---

## SHARED CONTEXT FOR ALL

### AWS Credentials (READ ONLY — do not commit these anywhere)
- Region: `us-east-1`
- Lambda: `janai-call-handler`
- API Gateway: `e1oy2y9gjj`
- S3 Bucket: `janai-documents`
- DynamoDB Tables: `janai-calls`, `janai-knowledge`, `janai-vectors`, `janai-users`

### Key Files
| File | What it is |
|---|---|
| `lambdas/call_handler/handler.py` | Entire backend in one file — all Lambda endpoints |
| `website/src/pages/TryPage.jsx` | The Try JanAI page (Call Me Back + Live Call tabs) |
| `website/src/App.jsx` | React router — add new pages here |
| `scripts/deploy.py` | Packages + deploys Lambda to AWS |
| `scripts/seed_knowledge.py` | Adds entries to DynamoDB RAG tables |
| `.env.example` | All required env var names (copy to `.env`, fill values) |

### How to Deploy Backend Changes
```powershell
# Set AWS credentials (ask jatin)
$env:AWS_ACCESS_KEY_ID="[REDACTED]"
$env:AWS_SECRET_ACCESS_KEY="[REDACTED]"
python scripts/deploy.py
```

### How to Run Frontend Locally
```powershell
cd website
npm install      # first time only
npx vite         # starts on localhost:3000 (or 3001 if 3000 is busy)
```

### API Endpoints Reference
| Endpoint | Method | What it does |
|---|---|---|
| `/call/initiate` | POST | Triggers Twilio callback to a phone number |
| `/chat` | POST | Text/voice chat with JanAI AI (no Twilio needed) |
| `/voice/incoming` | POST | Twilio webhook — start of phone call |
| `/voice/language` | POST | Twilio webhook — user selected language |
| `/voice/gather` | POST | Twilio webhook — user spoke, process and reply |
| `/auth/register` | POST | Create user account |
| `/auth/login` | POST | Login, returns JWT |
| `/profile` | GET/POST | User profile |

### Chat API — Quick Test
```powershell
Invoke-RestMethod -Uri "https://e1oy2y9gjj.execute-api.us-east-1.amazonaws.com/prod/chat" `
  -Method POST -ContentType "application/json" `
  -Body '{"message":"PM Kisan kya hai?","language":"hi","session_id":"test-1"}'
```

---

*Last updated: March 5, 2026 — Ask jatin if anything is unclear before starting.*
