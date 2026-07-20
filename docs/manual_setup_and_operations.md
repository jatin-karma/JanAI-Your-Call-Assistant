# 🛠️ JanAI — Manual Setup, Configuration & Operations Guide

This guide details all the **manual setup steps, API keys, webhook configurations, and operational workflows** required to run, test, and deploy JanAI locally and in production.

---

## 1. 🔑 Required Environment Variables (`.env`)

Create a `.env` file in the project root directory (`d:\Downloads\JanAI\JanAI\.env`) with the following structure:

```env
# --- AWS Credentials ---
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1

# --- Twilio Configuration ---
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+18312530646
TWILIO_TWIML_APP_SID=your_twiml_app_sid
TWILIO_API_KEY_SID=your_api_key_sid
TWILIO_API_KEY_SECRET=your_api_key_secret

# --- Speech & Voice Providers ---
SARVAM_API_KEY=your_sarvam_api_key
# Optional: Set to 'cartesia' for ultra-low latency (40ms TTFA)
TTS_PROVIDER=sarvam
CARTESIA_API_KEY=your_cartesia_api_key_here

# --- LLM & AI Models ---
LLM_PROVIDER=bedrock
BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
OPENAI_API_KEY=your_openai_api_key_here

# --- Live Data APIs ---
# Mandatory for live government Mandi / Agmarknet prices
DATA_GOV_API_KEY=your_data_gov_in_api_key

# --- DynamoDB Tables ---
DYNAMODB_CALLS_TABLE=janai_calls
DYNAMODB_KNOWLEDGE_TABLE=janai_knowledge
DYNAMODB_VECTORS_TABLE=janai_vectors
DYNAMODB_USERS_TABLE=janai_users
DYNAMODB_PHONE_PROFILES_TABLE=janai_phone_profiles
DYNAMODB_ACTIONS_TABLE=janai_actions

# --- S3 & Storage ---
S3_DOCUMENTS_BUCKET=janai-documents-2026

# --- App Settings ---
APP_ENV=development
LOG_LEVEL=INFO
```

---

## 2. 📞 Manual Twilio Console Configuration

To route incoming phone calls from your Twilio number to JanAI:

1. Log in to [Twilio Console](https://console.twilio.com/).
2. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**.
3. Click on your phone number (`+1 831 253 0646`).
4. Scroll down to **Voice & Fax**:
   * **A Call Comes In**: Select `Webhook`.
   * **URL**: Set to your production API Gateway endpoint:
     ```
     https://7hrrqf2fol.execute-api.us-east-1.amazonaws.com/prod/voice/incoming
     ```
   * **HTTP Method**: Set to `HTTP POST`.
5. Click **Save**.

---

## 3. 💻 Local Testing & Server Execution

### A. Run Python Local Server
Every time you modify backend code in Python (`lambdas/call_handler/handler.py` or `lambdas/web_agent/handler.py`), **manually restart** the Python server so changes reload in memory:

```bash
# In project root (d:\Downloads\JanAI\JanAI):
python scripts/local_server.py
```

### B. Run React Frontend Dev Server
```bash
# In website directory:
cd website
npm run dev
```

### C. Testing via Browser Simulator
Navigate in your browser to:
```
http://localhost:5173/sim
```
* Click **Start Call**.
* This simulator routes HTTP POST requests directly to `http://localhost:8000` (your local server).

---

## 4. 🌐 Deploying Updates to AWS & Vercel

### A. Deploy Python Backend to AWS Lambda (One-Line Script)
Whenever you want to deploy code changes to production AWS Lambda:

```powershell
# Deploy both call handler and web agent Lambdas automatically:
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1
```

### B. Deploy Frontend to Vercel
```powershell
cd website
vercel --prod
```

---

## 5. 📚 Manual Knowledge Ingestion for RAG

To add or update Government Schemes in the RAG Vector Knowledge Base:

1. Open [`scripts/seed_knowledge.py`](file:///d:/Downloads/JanAI/JanAI/scripts/seed_knowledge.py).
2. Append your new scheme definition to the `SCHEMES` array:
   ```python
   {
       "scheme_id": "new-scheme-id",
       "name_en": "Scheme Name",
       "name_hi": "योजना का नाम",
       "text_en": "English summary...",
       "text_hi": "हिंदी विवरण...",
       "eligibility_en": "Eligibility criteria...",
       "how_to_apply_en": "Application steps...",
       "documents_en": "Required documents...",
       "helpline": "1800-XXX-XXXX",
       "website": "scheme.gov.in"
   }
   ```
3. Run the vector embedding script manually:
   ```bash
   python scripts/seed_knowledge.py
   ```
   *This computes vector embeddings using AWS Bedrock Titan (`amazon.titan-embed-text-v2:0`) and saves them to DynamoDB `janai_vectors`.*

---

## ⏪ Rollback Procedures

If any production deployment encounters issues:

1. **Lambda Rollback (Git method):**
   ```powershell
   git checkout ac3d6ad -- lambdas/call_handler/handler.py
   powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1 -CallHandler
   ```
2. **Frontend Rollback (Vercel Dashboard):**
   * Go to [vercel.com/dashboard](https://vercel.com/dashboard) → `janai` project → **Deployments**.
   * Find the previous working deployment → click `...` → **Promote to Production**.
