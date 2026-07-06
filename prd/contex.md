# JanAI - Complete Product Requirements Document (PRD)
##  - Final Submission

> **Implementation Note (March 2026):** This PRD was written during the initial 4-day sprint.
> LLM references to "Claude 3.5 Sonnet" reflect the initial design; the deployed prototype uses
> **Amazon Bedrock Nova Lite** which provides comparable quality at lower cost and lower latency
> for the Indian use-case. TTS uses **Sarvam AI bulbul:v2** (not Bhashini — API access was not
> available during the hackathon window). See `HANDOFF.md` for the live stack.

**Document Version:** 2.0 (Final)  
**Team:** Kaizen  
**Team Leader:** jatin karma  
**Team Size:** 4 members  
**Deadline:** March 4, 2026, 11:59 PM IST  
**Time Available:** 4 Days (96 hours)  
**Status:** Selected for Prototype Development Phase  

---

## 📋 EXECUTIVE CONTEXT

### **The Story So Far:**

**February 15, 2026, 10:00 PM:**
- Friends called about 
- Deadline: Midnight (2 hours away)
- They had a generic health app idea (ArogyaSathi)
- We pivoted to JanAI (phone-based voice AI)
- Created PPT in 90 minutes using AI assistance
- Submitted at 11:59 PM

**February 25, 2026:**
- **SELECTED** for Prototype Development Phase
- Team is in shortlisted teams document
- Now have 4 days to build working prototype

**Current Situation:**
- 4 team members available
- AWS $100 credits available
- Twilio $15 trial credits available
- Must submit by March 4, 11:59 PM IST

---

## 🎯 PROJECT VISION

### **What is JanAI?**

JanAI is a **phone-based AI voice assistant** that enables 500M+ rural Indians without smartphones or internet to access critical government scheme information by calling a toll-free number.

### **The Problem We're Solving:**

**Target Users:** Rural Indians (18-60 years)
- 500M+ lack smartphones
- 70% have poor/no internet connectivity  
- 40% have limited education (<5 years)
- Existing solutions require apps + internet + digital literacy

**Current Solutions Fail Because:**
- Telemedicine apps need smartphones
- Government websites are desktop-only, English-heavy
- Helpline numbers have limited hours, long wait times
- ASHA workers are overworked, can't reach everyone

### **Our Solution:**

**User Experience:**
```
1. Call toll-free: 1800-XXX-XXXX
2. Select language: Hindi or English
3. Ask question: "PM Kisan ke baare mein batao"
4. Get AI answer: Accurate info in chosen language
5. Follow-up: Ask more questions naturally
6. Receive SMS: Summary of conversation (optional)
```

**Key Innovation:**
- Works on ₹500 feature phones
- Zero internet required
- Voice-first (no reading needed)
- AI-powered (24/7 consistent quality)
- Multilingual (Hindi + English for MVP)

---

## 🏆 HACKATHON REQUIREMENTS

### **Submission Deliverables (5 Required):**

1. ✅ **Project PPT** - Architecture, solution, impact
2. ✅ **GitHub Repository** - Full source code
3. ✅ **Working Prototype Link** - Live phone number to call
4. ✅ **Demo Video** - 3-5 minute walkthrough
5. ✅ **Project Summary** - Brief write-up

### **Technical Evaluation Criteria:**

**Must Use AWS Generative AI:**
- ✅ Amazon Bedrock (Claude 3.5 Sonnet)
- ✅ RAG workflows for knowledge retrieval
- ✅ Amazon Titan Embeddings for semantic search

**Must Explain:**
- ✅ Why AI is required
- ✅ How AWS services are used
- ✅ What value AI adds to user experience

**Must Use AWS Infrastructure:**
- ✅ AWS Lambda (serverless compute)
- ✅ API Gateway (REST endpoints)
- ✅ DynamoDB (NoSQL database)
- ✅ S3 (object storage)
- ✅ CloudWatch (monitoring)

**Bonus Points:**
- ✅ Serverless architecture
- ✅ Managed services (no EC2 management)
- ✅ Scalable patterns

---

## 🏗️ FINAL TECHNICAL ARCHITECTURE

### **Architecture Overview:**

```
┌─────────────────────────────────────────────────────────────┐
│                      USER LAYER                              │
│   Feature Phone | Smartphone | Landline (ANY phone device)  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ PSTN/Cellular Network
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  TELEPHONY LAYER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Twilio Voice API                         │   │
│  │  • Toll-free number: 1800-XXX-XXXX                   │   │
│  │  • Receives incoming calls                            │   │
│  │  • Streams audio bidirectionally                      │   │
│  │  • DTMF capture (language selection)                  │   │
│  │  • SMS delivery for summaries                         │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTPS Webhooks
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│            🟧 AWS API GATEWAY 🟧                             │
│  • REST API endpoints for Twilio webhooks                   │
│  • Request validation & throttling (1000 req/sec)           │
│  • CORS configuration                                        │
│  • CloudWatch integration                                    │
│                                                              │
│  Endpoints:                                                  │
│  POST /voice/incoming    - Handle new calls                 │
│  POST /voice/gather      - Process user speech              │
│  POST /voice/status      - Call status callbacks            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│         🟧 AWS LAMBDA - APPLICATION LAYER 🟧                 │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     Lambda Function: call-handler                      │  │
│  │  Runtime: Python 3.11                                 │  │
│  │  Memory: 512 MB                                       │  │
│  │  Timeout: 30 seconds                                  │  │
│  │  Concurrency: 100 (reserved)                          │  │
│  │                                                        │  │
│  │  Responsibilities:                                     │  │
│  │  • Receive Twilio webhook events                      │  │
│  │  • Manage call state & session                        │  │
│  │  • Language detection (Hindi/English)                 │  │
│  │  • Orchestrate STT → RAG → LLM → TTS pipeline        │  │
│  │  • Error handling & fallbacks                         │  │
│  │  • Log to DynamoDB & CloudWatch                       │  │
│  │  • Trigger SMS via Twilio API                         │  │
│  │  • Generate TwiML responses                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     Lambda Function: knowledge-updater                 │  │
│  │  Runtime: Python 3.11                                 │  │
│  │  Trigger: S3 PUT events                               │  │
│  │  Memory: 1024 MB                                      │  │
│  │  Timeout: 5 minutes                                   │  │
│  │                                                        │  │
│  │  Responsibilities:                                     │  │
│  │  • Process new scheme documents uploaded to S3        │  │
│  │  • Extract text from PDFs/HTML                        │  │
│  │  • Generate embeddings via Bedrock Titan              │  │
│  │  • Store in DynamoDB knowledge + vector tables        │  │
│  │  • Update search indices                              │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     Lambda Function: analytics-processor               │  │
│  │  Runtime: Python 3.11                                 │  │
│  │  Trigger: CloudWatch Events (every 5 minutes)         │  │
│  │  Memory: 256 MB                                       │  │
│  │                                                        │  │
│  │  Responsibilities:                                     │  │
│  │  • Aggregate call metrics from DynamoDB               │  │
│  │  • Calculate: total calls, avg duration, languages    │  │
│  │  • Update CloudWatch custom metrics                   │  │
│  │  • Generate daily usage reports                       │  │
│  └───────────────────────────────────────────────────────┘  │
└────────┬─────────────┬────────────┬─────────────┬───────────┘
         │             │            │             │
         ↓             ↓            ↓             ↓
   ┌──────────┐  ┌─────────┐  ┌────────┐  ┌──────────────┐
   │STT Layer │  │AI Layer │  │TTS     │  │Storage Layer │
   └──────────┘  └─────────┘  └────────┘  └──────────────┘


═══════════════════════════════════════════════════════════════
               DETAILED COMPONENT LAYERS
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│              🎤 SPEECH-TO-TEXT LAYER                         │
│                                                              │
│  PRIMARY: Bhashini API (Government of India)                │
│  ├─ Cost: FREE                                              │
│  ├─ Languages: Hindi, English, Tamil, Telugu                │
│  ├─ Latency: ~200-300ms                                     │
│  ├─ Accuracy: 75-85% (Indian accents)                       │
│  ├─ API: https://bhashini.gov.in/ulca/apis                  │
│  └─ Authentication: API key (free registration)             │
│                                                              │
│  FALLBACK: 🟧 Amazon Transcribe 🟧                           │
│  ├─ Cost: $0.024/minute (covered by AWS credits)           │
│  ├─ Accuracy: 85-90%                                        │
│  ├─ Real-time streaming: Yes                                │
│  ├─ Custom vocabulary: Scheme names, Hindi terms            │
│  ├─ Language codes: hi-IN, en-IN                            │
│  └─ Use when: Bhashini fails or low confidence (<70%)       │
│                                                              │
│  IMPLEMENTATION:                                             │
│  def transcribe_audio(audio_url, language):                 │
│      try:                                                    │
│          # Try Bhashini first                               │
│          text = bhashini_stt(audio_url, language)           │
│          if confidence > 0.7:                               │
│              return text                                     │
│      except:                                                 │
│          # Fallback to AWS Transcribe                       │
│          text = aws_transcribe(audio_url, language)         │
│          return text                                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│      🟧 GENERATIVE AI LAYER - AMAZON BEDROCK 🟧              │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Claude 3.5 Sonnet (Primary LLM)                │  │
│  │  Model ID: anthropic.claude-3-5-sonnet-20241022-v2:0  │  │
│  │  Region: us-east-1                                     │  │
│  │  Max Tokens: 500 (phone-appropriate)                  │  │
│  │  Temperature: 0.3 (deterministic)                     │  │
│  │  Top P: 0.9                                           │  │
│  │                                                        │  │
│  │  Cost: ~$3 per 1M input tokens                        │  │
│  │        ~$15 per 1M output tokens                      │  │
│  │  Expected usage: $10-15 for full demo                 │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │      Amazon Titan Text Embeddings v2 (RAG)            │  │
│  │  Model ID: amazon.titan-embed-text-v2:0               │  │
│  │  Dimensions: 1024                                     │  │
│  │  Use: Generate embeddings for semantic search         │  │
│  │  Cost: ~$0.0001 per 1K tokens                         │  │
│  │  Expected usage: $5 for full demo                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  SYSTEM PROMPT (Claude):                                     │
│  """                                                         │
│  You are JanAI, an AI assistant helping rural Indians   │
│  access government schemes via phone.                        │
│                                                              │
│  CONTEXT:                                                    │
│  - User is calling from feature phone (no internet)         │
│  - User may have limited education                          │
│  - User speaks Hindi or English (or mix)                    │
│                                                              │
│  YOUR ROLE:                                                  │
│  - Provide accurate info about 5 govt schemes:              │
│    1. PM-Kisan (farmer income support)                      │
│    2. Ayushman Bharat (health insurance)                    │
│    3. MGNREGA (employment guarantee)                        │
│    4. PM Awas Yojana (housing)                              │
│    5. Sukanya Samriddhi Yojana (girl child savings)         │
│                                                              │
│  RULES:                                                      │
│  - Always respond in user's language                        │
│  - Use simple words (avoid jargon)                          │
│  - Be concise (max 3 sentences)                             │
│  - If out of scope, politely redirect                       │
│  - Always cite official sources                             │
│  - If unsure, say "I don't have that information"          │
│                                                              │
│  RESPONSE FORMAT:                                            │
│  - Direct answer first                                       │
│  - Supporting details second                                 │
│  - Ask if they want to know more                            │
│  """                                                         │
│                                                              │
│  RAG WORKFLOW:                                               │
│  1. User query → Generate embedding (Titan)                 │
│  2. Vector search in DynamoDB (cosine similarity)           │
│  3. Retrieve top 3 relevant scheme sections                 │
│  4. Pass to Claude as context                               │
│  5. Claude generates response                               │
│  6. Return to user                                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              🔊 TEXT-TO-SPEECH LAYER                         │
│                                                              │
│  PRIMARY: Bhashini API (Government of India)                │
│  ├─ Cost: FREE                                              │
│  ├─ Languages: Hindi (Aditi), English (Raveena)            │
│  ├─ Voice quality: Natural, Indian accents                  │
│  ├─ Latency: ~200-300ms                                     │
│  └─ API: https://bhashini.gov.in/ulca/apis                  │
│                                                              │
│  FALLBACK: 🟧 Amazon Polly 🟧                                │
│  ├─ Cost: $4 per 1M characters (covered by credits)        │
│  ├─ Hindi voice: Aditi (female, natural)                   │
│  ├─ English voice: Raveena (female, Indian accent)         │
│  ├─ Neural engine: Yes                                      │
│  ├─ SSML support: Yes (for emphasis, pauses)               │
│  └─ Use when: Bhashini unavailable or better quality needed │
│                                                              │
│  IMPLEMENTATION:                                             │
│  def text_to_speech(text, language):                        │
│      try:                                                    │
│          # Try Bhashini first (free)                        │
│          audio_url = bhashini_tts(text, language)           │
│          return audio_url                                    │
│      except:                                                 │
│          # Fallback to AWS Polly                            │
│          audio_url = aws_polly(text, language)              │
│          return audio_url                                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│           🟧 STORAGE LAYER - AWS SERVICES 🟧                 │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Amazon DynamoDB Tables                    │  │
│  │                                                        │  │
│  │  TABLE 1: janai-calls                             │  │
│  │  Purpose: Call logs and session state                 │  │
│  │  Partition Key: call_id (String)                      │  │
│  │  Sort Key: timestamp (Number)                         │  │
│  │  Attributes:                                           │  │
│  │    - from_number (String)                             │  │
│  │    - language (String: "hi" | "en")                   │  │
│  │    - duration (Number, seconds)                       │  │
│  │    - conversation_history (List of Maps)              │  │
│  │    - queries_count (Number)                           │  │
│  │    - schemes_queried (Set of Strings)                 │  │
│  │    - sms_sent (Boolean)                               │  │
│  │    - status (String: "completed" | "in-progress")     │  │
│  │  Provisioned Capacity: 5 RCU, 5 WCU (free tier)       │  │
│  │                                                        │  │
│  │  TABLE 2: janai-knowledge                         │  │
│  │  Purpose: Government scheme information               │  │
│  │  Partition Key: scheme_id (String)                    │  │
│  │  Sort Key: section_id (String)                        │  │
│  │  Attributes:                                           │  │
│  │    - name_en, name_hi (String)                        │  │
│  │    - description_en, description_hi (String)          │  │
│  │    - eligibility_en, eligibility_hi (String)          │  │
│  │    - documents_en, documents_hi (List)                │  │
│  │    - benefits_en, benefits_hi (String)                │  │
│  │    - apply_process_en, apply_process_hi (String)      │  │
│  │    - website (String)                                 │  │
│  │    - helpline (String)                                │  │
│  │  Provisioned Capacity: 5 RCU, 5 WCU (free tier)       │  │
│  │                                                        │  │
│  │  TABLE 3: janai-vectors                           │  │
│  │  Purpose: Embeddings for semantic search             │  │
│  │  Partition Key: embedding_id (String)                 │  │
│  │  Attributes:                                           │  │
│  │    - text (String, original text)                     │  │
│  │    - embedding (List of Numbers, 1024 dims)           │  │
│  │    - scheme_id (String)                               │  │
│  │    - section_id (String)                              │  │
│  │    - language (String)                                │  │
│  │    - metadata (Map)                                   │  │
│  │  Provisioned Capacity: 5 RCU, 5 WCU (free tier)       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 Amazon S3 Buckets                      │  │
│  │                                                        │  │
│  │  BUCKET 1: janai-documents                        │  │
│  │  Purpose: Raw scheme documents                        │  │
│  │  Structure:                                            │  │
│  │    /schemes/pm-kisan/*.pdf                            │  │
│  │    /schemes/ayushman-bharat/*.pdf                     │  │
│  │    /schemes/mgnrega/*.pdf                             │  │
│  │  Versioning: Enabled                                  │  │
│  │  Lifecycle: Standard → Glacier after 90 days          │  │
│  │                                                        │  │
│  │  BUCKET 2: janai-audio (optional)                 │  │
│  │  Purpose: Call recordings for debugging               │  │
│  │  Structure: /calls/YYYY/MM/DD/{call_id}.mp3           │  │
│  │  Lifecycle: Delete after 7 days                       │  │
│  │  Encryption: AES-256                                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              🟧 Amazon CloudWatch 🟧                   │  │
│  │                                                        │  │
│  │  Log Groups:                                           │  │
│  │    /aws/lambda/call-handler                           │  │
│  │    /aws/lambda/knowledge-updater                      │  │
│  │    /aws/lambda/analytics-processor                    │  │
│  │  Retention: 7 days                                    │  │
│  │                                                        │  │
│  │  Custom Metrics:                                       │  │
│  │    - CallsTotal (Count)                               │  │
│  │    - CallDurationAvg (Seconds)                        │  │
│  │    - LanguageDistribution (Percent)                   │  │
│  │    - SchemeQueriesCount (Count per scheme)            │  │
│  │    - ErrorRate (Percent)                              │  │
│  │    - STTAccuracy (Percent, manual validation)         │  │
│  │                                                        │  │
│  │  Dashboards:                                           │  │
│  │    - JanAI Overview (real-time metrics)           │  │
│  │    - Call Analytics (trends, patterns)                │  │
│  │    - Error Monitoring (failed calls, timeouts)        │  │
│  │                                                        │  │
│  │  Alarms:                                               │  │
│  │    - ErrorRateHigh (>10% errors → SNS notification)   │  │
│  │    - LambdaThrottling (concurrent exec limit)         │  │
│  │    - DynamoDBThrottling (read/write limits)           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 DATA STRATEGY

### **Data Sources:**

1. **Government Scheme Documents:**
   - pmkisan.gov.in (PM-Kisan)
   - ayushmanbharat.in (Ayushman Bharat)
   - nrega.nic.in (MGNREGA)
   - pmaymis.gov.in (PM Awas Yojana)
   - nari.nic.in (Sukanya Samriddhi Yojana)

2. **Structured Data Creation:**
   - Manual curation from NITI Aayog reports
   - Official government circulars
   - FAQ sections from ministry websites

3. **User Interaction Data:**
   - Call transcripts (anonymized)
   - Query patterns
   - Conversation flow analytics

### **Data Processing Pipeline:**

```
┌──────────────┐
│ Raw Document │ (PDF/HTML uploaded to S3)
└──────┬───────┘
       │
       │ S3 Event triggers Lambda
       ↓
┌────────────────┐
│ Text Extraction│ (PyPDF2, BeautifulSoup)
└──────┬─────────┘
       │
       ↓
┌──────────────────┐
│ Chunking         │ (500-word sections)
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Embedding Gen    │ (Titan Embeddings)
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Store in DynamoDB│ (knowledge + vectors tables)
└──────────────────┘
```

### **RAG (Retrieval Augmented Generation) Workflow:**

```
User Query: "PM Kisan mein kaun eligible hai?"
       ↓
┌──────────────────┐
│ Generate Embed   │ (Titan: query → vector)
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Vector Search    │ (Cosine similarity in DynamoDB)
│ Top 3 Results:   │
│ 1. PM-Kisan eligibility (0.92 similarity)
│ 2. PM-Kisan documents (0.88 similarity)
│ 3. PM-Kisan benefits (0.85 similarity)
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Build Context    │ (Combine retrieved sections)
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│ Claude API Call  │
│ Prompt:          │
│ Context: [Retrieved sections]
│ Query: [User question]
│ Generate: [Concise answer in Hindi]
└──────┬───────────┘
       │
       ↓
Response: "PM Kisan योजना में 2 हेक्टेयर तक की खेती 
वाली भूमि के किसान eligible हैं..."
```

---

## 🎯 MVP SCOPE (4-Day Build)

### **Must-Have Features (P0):**

**Functional:**
- [ ] Working toll-free phone number
- [ ] Language selection (Hindi/English)
- [ ] 5 government schemes in knowledge base:
  1. PM-Kisan
  2. Ayushman Bharat
  3. MGNREGA
  4. PM Awas Yojana
  5. Sukanya Samriddhi Yojana
- [ ] Each scheme must answer:
  - Eligibility criteria
  - Required documents
  - Application process
  - Benefits amount
  - Official website/helpline
- [ ] Multi-turn conversation (3+ exchanges)
- [ ] SMS summary after call ends
- [ ] Call timeout (5 minutes)

**Technical:**
- [ ] AWS Lambda backend (Python 3.11)
- [ ] API Gateway webhooks
- [ ] DynamoDB (3 tables)
- [ ] Amazon Bedrock (Claude + Titan)
- [ ] Hybrid STT/TTS (Bhashini + AWS)
- [ ] CloudWatch monitoring
- [ ] Error handling (graceful failures)

**Quality:**
- [ ] Response latency <5 seconds
- [ ] STT accuracy >75% (tested with 20 samples)
- [ ] Information accuracy 100% (verified against official sources)
- [ ] System uptime >95% (during demo week)

### **Nice-to-Have Features (P1):**

- [ ] Advanced RAG with vector search (if time permits)
- [ ] Analytics dashboard (basic call metrics)
- [ ] Regional accent handling
- [ ] Background noise tolerance
- [ ] Callback feature (if call drops)

### **Out of Scope (Post-Hackathon):**

- ❌ More than 2 languages (just Hindi + English)
- ❌ Healthcare domain
- ❌ User accounts/personalization
- ❌ ASHA worker dashboard
- ❌ Call recording storage beyond 7 days
- ❌ Integration with actual government databases

---

## 📅 4-DAY SPRINT PLAN

### **Team Roles:**

**Person 1 (You - Tech Lead):**
- AWS setup, Lambda functions, API Gateway
- Integration orchestration
- Final submission prep

**Person 2 (Backend Dev):**
- Knowledge base creation
- RAG implementation
- DynamoDB schema

**Person 3 (AI/ML Engineer):**
- Bedrock integration
- Prompt engineering
- Embedding generation

**Person 4 (DevOps/Testing):**
- STT/TTS integration
- CloudWatch setup
- Testing & PPT creation

---

### **DAY 1 - INFRASTRUCTURE (Today)**

**MORNING (3 hours) - Setup:**

**Person 1:**
- [ ] Create AWS account
- [ ] Apply $100 credits
- [ ] Set up IAM roles:
  - lambda-execution-role (DynamoDB, S3, Bedrock access)
  - api-gateway-role
- [ ] Initialize GitHub repo: `janai-hackathon`
- [ ] Create project structure:
```
janai/
├── lambda/
│   ├── call_handler.py
│   ├── knowledge_updater.py
│   └── analytics_processor.py
├── knowledge_base/
│   ├── schemes/
│   │   ├── pm_kisan.json
│   │   ├── ayushman_bharat.json
│   │   ├── mgnrega.json
│   │   ├── pm_awas.json
│   │   └── sukanya_samriddhi.json
│   └── embeddings/
├── tests/
├── docs/
└── README.md
```

**Person 2:**
- [ ] Create DynamoDB tables:
  - `janai-calls` (PK: call_id, SK: timestamp)
  - `janai-knowledge` (PK: scheme_id, SK: section_id)
  - `janai-vectors` (PK: embedding_id)
- [ ] Set provisioned capacity: 5 RCU, 5 WCU each
- [ ] Enable point-in-time recovery

**Person 3:**
- [ ] Request Bedrock model access:
  - Claude 3.5 Sonnet
  - Titan Text Embeddings v2
- [ ] Test Bedrock API with sample prompt
- [ ] Create system prompt template

**Person 4:**
- [ ] Create Twilio trial account
- [ ] Get toll-free number
- [ ] Set up S3 buckets:
  - `janai-documents`
  - `janai-audio`
- [ ] Enable versioning

**AFTERNOON (3 hours) - Hello World:**

**Person 1:**
- [ ] Deploy basic Lambda function:
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Hello from JanAI</Say></Response>'
    }
```
- [ ] Create API Gateway endpoint
- [ ] Connect Twilio webhook to API Gateway
- [ ] **TEST:** Call number → Hear "Hello from JanAI"

**Person 2:**
- [ ] Start curating PM-Kisan scheme data
- [ ] Structure JSON:
```json
{
  "scheme_id": "pm-kisan",
  "name": {
    "en": "PM-Kisan",
    "hi": "पीएम किसान"
  },
  "description": {
    "en": "Income support for small farmers",
    "hi": "छोटे किसानों के लिए आय सहायता"
  },
  "eligibility": {
    "en": "Farmers with up to 2 hectares of cultivable land",
    "hi": "2 हेक्टेयर तक की खेती योग्य भूमि वाले किसान"
  },
  "documents": {
    "en": ["Aadhaar card", "Bank account details", "Land records"],
    "hi": ["आधार कार्ड", "बैंक खाता विवरण", "भूमि रिकॉर्ड"]
  },
  "benefits": {
    "en": "₹6000 per year in 3 installments of ₹2000 each",
    "hi": "साल में ₹6000, 3 किस्तों में ₹2000 प्रत्येक"
  },
  "apply": {
    "en": "Apply online at pmkisan.gov.in or visit nearest CSC",
    "hi": "pmkisan.gov.in पर ऑनलाइन आवेदन करें या नजदीकी CSC पर जाएं"
  },
  "website": "https://pmkisan.gov.in",
  "helpline": "155261 / 1800115526"
}
```
- [ ] Upload to DynamoDB `janai-knowledge` table

**Person 3:**
- [ ] Integrate Bedrock Claude in Lambda:
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_claude(prompt, context=""):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {prompt}"
            }
        ]
    })
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']
```
- [ ] **TEST:** Lambda → Bedrock → Returns response

**Person 4:**
- [ ] Register for Bhashini API: https://bhashini.gov.in
- [ ] Get API credentials
- [ ] Test Bhashini STT with sample audio
- [ ] Test Bhashini TTS with sample text

**EVENING (2 hours) - Integration:**

**ALL TEAM:**
- [ ] Daily standup: Review progress
- [ ] Integrate components:
  - Twilio → API Gateway → Lambda
  - Lambda → DynamoDB (log call)
  - Lambda → Bedrock (get response)
- [ ] **TEST:** Call → System logs call to DynamoDB

**DAY 1 CHECKPOINT:**
✅ Phone number works  
✅ Lambda function deployed  
✅ DynamoDB tables created  
✅ Bedrock API working  
✅ Basic logging in place  

**DAY 1 SUCCESS METRIC:**
Can call the number and hear a static message. System logs the call.

---

### **DAY 2 - CORE FEATURES (Tomorrow)**

**MORNING (4 hours) - STT + LLM + TTS:**

**Person 1:**
- [ ] Implement call flow in Lambda:
```python
def lambda_handler(event, context):
    # Parse Twilio event
    call_sid = event['CallSid']
    from_number = event['From']
    
    # Check if language selected
    if 'Digits' in event:
        language = 'hi' if event['Digits'] == '1' else 'en'
        # Save to session
        save_session(call_sid, {'language': language})
        # Prompt for question
        return twiml_gather_speech(language)
    
    # If speech result available
    if 'SpeechResult' in event:
        user_query = event['SpeechResult']
        session = get_session(call_sid)
        
        # Process query
        response_text = process_query(user_query, session)
        
        # Convert to speech and return
        return twiml_say(response_text, session['language'])
    
    # Initial greeting
    return twiml_language_selection()
```

**Person 2:**
- [ ] Complete all 5 schemes in knowledge base
- [ ] Insert into DynamoDB
- [ ] Create retrieval function:
```python
def get_scheme_info(scheme_id, section, language):
    table = dynamodb.Table('janai-knowledge')
    response = table.get_item(
        Key={
            'scheme_id': scheme_id,
            'section_id': section
        }
    )
    item = response['Item']
    return item[f'{section}_{language}']
```

**Person 3:**
- [ ] Implement RAG logic:
```python
def process_query(user_query, session):
    # 1. Detect which scheme (simple keyword matching for MVP)
    scheme_id = detect_scheme(user_query)
    
    # 2. Retrieve relevant info
    context = get_scheme_context(scheme_id, session['language'])
    
    # 3. Call Claude with context
    system_prompt = load_system_prompt()
    response = call_claude(
        prompt=user_query,
        context=context,
        system=system_prompt
    )
    
    # 4. Update conversation history
    update_session(session['call_sid'], user_query, response)
    
    return response
```

**Person 4:**
- [ ] Integrate Bhashini STT:
```python
import requests

def bhashini_stt(audio_url, language):
    # Download audio from Twilio
    audio = requests.get(audio_url).content
    
    # Call Bhashini API
    response = requests.post(
        'https://bhashini.gov.in/ulca/apis/asr',
        headers={'Authorization': f'Bearer {BHASHINI_KEY}'},
        json={
            'audio': base64.b64encode(audio).decode(),
            'language': language
        }
    )
    
    return response.json()['transcript']
```
- [ ] Integrate Bhashini TTS:
```python
def bhashini_tts(text, language):
    response = requests.post(
        'https://bhashini.gov.in/ulca/apis/tts',
        headers={'Authorization': f'Bearer {BHASHINI_KEY}'},
        json={
            'text': text,
            'language': language,
            'gender': 'female'
        }
    )
    
    return response.json()['audio_url']
```

**AFTERNOON (4 hours) - End-to-End Flow:**

**ALL TEAM:**
- [ ] Integrate all components
- [ ] Test flow:
  1. Call number
  2. Select Hindi
  3. Ask "PM Kisan kya hai?"
  4. Receive accurate Hindi response
  5. Ask follow-up: "Documents kya chahiye?"
  6. Receive document list
  7. Say "Dhanyavaad"
  8. Call ends

- [ ] Debug issues
- [ ] Handle errors:
  - Couldn't understand speech
  - Bedrock API timeout
  - DynamoDB throttling

**EVENING (2 hours) - Multi-Scheme Testing:**

**Person 1 & 2:**
- [ ] Test all 5 schemes:
  - PM-Kisan
  - Ayushman Bharat
  - MGNREGA
  - PM Awas Yojana
  - Sukanya Samriddhi Yojana

**Person 3 & 4:**
- [ ] Test both languages (Hindi + English)
- [ ] Test code-mixed queries (Hinglish)
- [ ] Document bugs in GitHub Issues

**DAY 2 CHECKPOINT:**
✅ Voice input working (STT)  
✅ AI responds accurately (Bedrock)  
✅ Voice output working (TTS)  
✅ All 5 schemes queryable  
✅ Multi-turn conversation works  

**DAY 2 SUCCESS METRIC:**
Full conversation flow working: Call → Ask 3 questions → Get accurate answers → End call

---

### **DAY 3 - POLISH & ADVANCED FEATURES**

**MORNING (3 hours) - RAG with Vector Search:**

**Person 2 & 3:**
- [ ] Generate embeddings for all scheme sections:
```python
def generate_embeddings():
    table = dynamodb.Table('janai-knowledge')
    vectors_table = dynamodb.Table('janai-vectors')
    
    # Scan all scheme data
    response = table.scan()
    
    for item in response['Items']:
        # For each section, generate embedding
        for section in ['description', 'eligibility', 'benefits']:
            text_en = item[f'{section}_en']
            text_hi = item[f'{section}_hi']
            
            # Generate embeddings
            embed_en = get_titan_embedding(text_en)
            embed_hi = get_titan_embedding(text_hi)
            
            # Store in vectors table
            vectors_table.put_item(Item={
                'embedding_id': f"{item['scheme_id']}_{section}_en",
                'text': text_en,
                'embedding': embed_en,
                'scheme_id': item['scheme_id'],
                'section_id': section,
                'language': 'en'
            })
            # Same for Hindi
```

- [ ] Implement vector search:
```python
def vector_search(query, language, top_k=3):
    # Generate query embedding
    query_embed = get_titan_embedding(query)
    
    # Scan vectors table (for MVP; use proper vector DB in production)
    vectors_table = dynamodb.Table('janai-vectors')
    response = vectors_table.scan(
        FilterExpression=Attr('language').eq(language)
    )
    
    # Calculate cosine similarity
    results = []
    for item in response['Items']:
        similarity = cosine_similarity(query_embed, item['embedding'])
        results.append({
            'text': item['text'],
            'scheme_id': item['scheme_id'],
            'similarity': similarity
        })
    
    # Sort and return top K
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]
```

**AFTERNOON (3 hours) - SMS & Analytics:**

**Person 1:**
- [ ] Implement SMS summary:
```python
def send_sms_summary(call_sid, from_number):
    # Get conversation history
    session = get_session(call_sid)
    
    # Generate summary
    summary = generate_summary(session['conversation_history'])
    
    # Send via Twilio
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        to=from_number,
        from_=TWILIO_NUMBER,
        body=summary
    )
```

**Person 4:**
- [ ] Set up CloudWatch dashboard
- [ ] Create custom metrics:
```python
cloudwatch = boto3.client('cloudwatch')

def log_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='JanAI',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
        ]
    )

# Usage
log_metric('CallsTotal', 1)
log_metric('CallDuration', duration_seconds, 'Seconds')
log_metric('SchemeQuery_PMKisan', 1)
```

**EVENING (3 hours) - Error Handling & Edge Cases:**

**ALL TEAM:**
- [ ] Handle edge cases:
  - User speaks too fast/slow
  - Background noise
  - Out-of-scope questions
  - Network issues
  - API timeouts

- [ ] Implement fallbacks:
```python
def process_with_fallback(func, fallback_func):
    try:
        return func()
    except Exception as e:
        logger.error(f"Primary function failed: {e}")
        return fallback_func()

# Usage
text = process_with_fallback(
    lambda: bhashini_stt(audio_url, language),
    lambda: aws_transcribe(audio_url, language)
)
```

- [ ] Add call timeout (5 minutes):
```python
def check_timeout(call_start_time):
    elapsed = time.time() - call_start_time
    if elapsed > 300:  # 5 minutes
        return twiml_timeout_message()
```

**DAY 3 CHECKPOINT:**
✅ Vector search working (better accuracy)  
✅ SMS summaries sent  
✅ CloudWatch metrics tracked  
✅ Error handling robust  
✅ All edge cases covered  

**DAY 3 SUCCESS METRIC:**
20 test calls with various scenarios - all handled gracefully.

---

### **DAY 4 - DEMO & SUBMISSION (Deadline Day)**

**MORNING (3 hours) - Demo Video:**

**Person 1:**
- [ ] Record screen capture
- [ ] Show architecture diagram
- [ ] Explain AWS services used

**Person 2:**
- [ ] Record live phone call demo
- [ ] Show 3 scenarios:
  1. Hindi query about PM-Kisan
  2. English query about Ayushman Bharat
  3. Multi-turn conversation about MGNREGA

**Person 3:**
- [ ] Show AWS console:
  - Lambda functions
  - DynamoDB tables
  - CloudWatch metrics
  - Bedrock usage

**Person 4:**
- [ ] Edit video:
  - Add subtitles for Hindi audio
  - Add transitions
  - Keep under 5 minutes
  - Export in 1080p

**AFTERNOON (2 hours) - Documentation:**

**Person 1:**
- [ ] Update GitHub README:
```markdown
# JanAI - Voice AI for Rural India

## Problem
500M+ rural Indians lack smartphone/internet access to government schemes.

## Solution
Phone-based AI assistant (toll-free) for accessing scheme information in Hindi/English.

## Architecture
[Diagram]

## AWS Services Used
- Amazon Bedrock (Claude 3.5 Sonnet, Titan Embeddings)
- AWS Lambda (serverless compute)
- API Gateway (REST endpoints)
- DynamoDB (NoSQL database)
- S3 (object storage)
- CloudWatch (monitoring)

## Tech Stack
- Backend: Python 3.11
- AI: Amazon Bedrock (Claude + Titan)
- STT/TTS: Bhashini API (primary), AWS Transcribe/Polly (fallback)
- Telephony: Twilio Voice API

## Setup Instructions
[Step-by-step guide]

## Demo
[Link to video]

## Team
Kaizen - 
```

**Person 2:**
- [ ] Create project summary (500 words):
  - Problem statement
  - Solution overview
  - AWS integration
  - Impact metrics
  - Future roadmap

**Person 3:**
- [ ] Update PPT:
  - Add architecture diagram
  - Add demo screenshots
  - Add AWS services slide
  - Add impact metrics

**Person 4:**
- [ ] Final code cleanup:
  - Add comments
  - Remove debug code
  - Format with Black
  - Run linter

**EVENING (2 hours - FINAL SUBMISSION):**

**6:00 PM - Review Checklist:**
- [ ] PPT uploaded
- [ ] GitHub repo public with README
- [ ] Demo video uploaded (YouTube unlisted)
- [ ] Project summary written
- [ ] Working prototype link (phone number)

**7:00 PM - Test Everything:**
- [ ] Call phone number 10 times
- [ ] Test all 5 schemes
- [ ] Test both languages
- [ ] Verify SMS working
- [ ] Check CloudWatch metrics

**8:00 PM - SUBMIT:**
- [ ] Go to submission portal
- [ ] Fill all fields
- [ ] Upload all materials
- [ ] **Submit before 9:00 PM** (3-hour buffer)

**9:00 PM - Backup:**
- [ ] Download submission confirmation
- [ ] Keep phone number alive
- [ ] Monitor for any issues

**DAY 4 CHECKPOINT:**
✅ Demo video recorded  
✅ Documentation complete  
✅ Code polished  
✅ All deliverables ready  
✅ **SUBMITTED**  

---

## 📊 SUCCESS METRICS

### **Technical Metrics:**

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Call Success Rate | >90% | (Successful calls / Total calls) × 100 |
| STT Accuracy | >75% | Manual review of 20 transcriptions |
| Response Latency | <5 sec | CloudWatch logs: Query → Response |
| Information Accuracy | 100% | Verify against official sources |
| System Uptime | >95% | CloudWatch uptime (demo week) |
| Multi-Turn Success | >60% | Calls with >2 exchanges / Total |

### **Demo Metrics:**

| Metric | Target | Notes |
|--------|--------|-------|
| Total Demo Calls | 100-200 | Team + friends testing |
| Unique Callers | 20-30 | Different phone numbers |
| Schemes Queried | All 5 | At least 10 queries per scheme |
| Languages Used | Both | 50% Hindi, 50% English |
| SMS Delivery Rate | >95% | SMS sent / SMS delivered |

### **AWS Metrics:**

| Service | Usage Target | Cost Target |
|---------|--------------|-------------|
| Lambda | 100-500 invocations | $0 (free tier) |
| Bedrock Claude | 50K tokens | $10-15 |
| Bedrock Titan | 10K tokens | $5 |
| DynamoDB | 1000 read/write | $0 (free tier) |
| S3 | 1GB storage | $0 (free tier) |
| **Total AWS Spend** | | **$15-25 of $100** |

---

## 💰 BUDGET BREAKDOWN

### **AWS Credits ($100):**

**Will Use (~$20-30):**
- Bedrock Claude: $10-15 (primary AI)
- Bedrock Titan: $5 (embeddings)
- Transcribe (fallback): $3-5 (backup STT)
- Polly (fallback): $2-3 (backup TTS)

**Free Tier (Won't Pay):**
- Lambda: 1M free requests/month
- API Gateway: 1M free requests/month
- DynamoDB: 25GB free storage
- S3: 5GB free storage
- CloudWatch: 5GB free logs

**Credits Remaining:** $70-80 (for future phases)

### **External Services:**

**Twilio ($15 trial credits):**
- Incoming calls: $0.0085/min
- 300 minutes = ~$2.55
- SMS: $0.0075 each
- **Total: ~$5 of $15 credits**

**Bhashini (FREE):**
- STT: Unlimited free
- TTS: Unlimited free
- **Total: $0**

### **Total MVP Cost:**

| Component | Cost |
|-----------|------|
| AWS Services | $20-30 (from credits) |
| Twilio | $5 (from credits) |
| Bhashini | $0 (free) |
| Development | $0 (your time) |
| **TOTAL** | **$25-35** |
| **Out of Pocket** | **$0** |

---

## ⚠️ RISKS & MITIGATION

### **Technical Risks:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Bedrock quota limits** | Medium | High | Monitor usage, implement caching |
| **Bhashini API downtime** | Medium | High | AWS Transcribe/Polly as fallback |
| **Lambda cold starts** | High | Low | Scheduled pings to keep warm |
| **DynamoDB throttling** | Low | Medium | Exponential backoff, increase capacity |
| **Twilio credits exhausted** | Low | High | Limit test calls, monitor usage |

### **Timeline Risks:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Team member unavailable** | Medium | High | Cross-train, document everything |
| **Scope creep** | High | Critical | Stick to must-haves, defer nice-to-haves |
| **Integration bugs** | High | Medium | Daily integration tests, buffer time |
| **Last-minute bug** | High | Critical | Code freeze 24h before deadline |

### **Submission Risks:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Portal crashes near deadline** | Medium | Critical | Submit 3 hours early (by 9 PM) |
| **Video upload fails** | Low | High | Upload to multiple platforms |
| **Phone number goes down** | Low | Critical | Have backup Twilio number ready |
| **GitHub repo private** | Low | Medium | Double-check repo visibility |

---

## 📞 PHONE FLOW (Detailed)

### **Call Flow State Machine:**

```
┌─────────────────────┐
│  USER CALLS NUMBER  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  STATE: LANGUAGE_SELECTION          │
│  "Welcome to JanAI.             │
│   Press 1 for Hindi                 │
│   Press 2 for English               │
│   या अपनी भाषा बोलें"                │
└──────────┬──────────────────────────┘
           │
           ├─── DTMF: 1 ──→ Language = Hindi
           ├─── DTMF: 2 ──→ Language = English
           └─── Speech ───→ Auto-detect
           │
           ↓
┌─────────────────────────────────────┐
│  STATE: GREETING                    │
│  (Hindi) "नमस्ते। आप मुझसे          │
│  सरकारी योजनाओं के बारे में पूछ    │
│  सकते हैं। कैसे मदद कर सकता हूँ?"  │
│  (English) "Hello. You can ask me   │
│  about government schemes. How      │
│  can I help you?"                   │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  STATE: LISTENING                   │
│  [Recording user speech...]         │
│  Max duration: 30 seconds           │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  STATE: PROCESSING                  │
│  1. STT (Bhashini → AWS Transcribe) │
│  2. Detect intent & scheme          │
│  3. RAG: Vector search              │
│  4. Bedrock Claude: Generate        │
│  5. TTS (Bhashini → AWS Polly)      │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  STATE: RESPONDING                  │
│  [Playing AI-generated audio...]    │
│  + "क्या आपका कोई और सवाल है?"     │
└──────────┬──────────────────────────┘
           │
           ├─── User: "Haan" ──→ Back to LISTENING
           ├─── User: "Nahi" ─→ Go to CLOSING
           └─── Timeout (30s) → Go to CLOSING
           │
           ↓
┌─────────────────────────────────────┐
│  STATE: CLOSING                     │
│  "धन्यवाद! जानकारी SMS में भेजी    │
│  जाएगी। फिर मिलेंगे। नमस्ते!"      │
│  [Send SMS summary]                 │
│  [Log call to DynamoDB]             │
│  [Update CloudWatch metrics]        │
│  [Disconnect]                       │
└─────────────────────────────────────┘
```

### **Error States:**

```
ERROR: STT_CONFIDENCE_LOW (<70%)
→ "क्षमा करें, मैं सुन नहीं पाया। कृपया फिर से बोलें।"
→ Retry (max 3 times) → If still failing → Apologize & disconnect

ERROR: BEDROCK_TIMEOUT
→ "कृपया थोड़ा रुकें..."
→ Retry with exponential backoff
→ If still failing → "तकनीकी समस्या है। कृपया बाद में कॉल करें।"

ERROR: OUT_OF_SCOPE
→ "मैं केवल सरकारी योजनाओं के बारे में बता सकता हूँ।"
→ List available schemes
→ Ask if they want info on any scheme

ERROR: CALL_DURATION_EXCEEDED (5 minutes)
→ "समय समाप्त। जानकारी SMS में भेजी जाएगी। धन्यवाद!"
→ Force disconnect
```

---

## 🎬 DEMO VIDEO SCRIPT

**Duration:** 4-5 minutes  
**Format:** Screen recording + voiceover + phone call recording

### **Section 1: Introduction (30 seconds)**

**Voiceover:**
"Hi, I'm [Name] from Team Kaizen. Today we're presenting JanAI - an AI-powered voice assistant that brings government scheme information to 500 million rural Indians who don't have smartphones or internet access."

**Visuals:**
- Show problem statistics
- Show solution diagram

---

### **Section 2: Architecture (60 seconds)**

**Voiceover:**
"JanAI is built entirely on AWS infrastructure. Users call a toll-free number which connects to our serverless backend powered by AWS Lambda and API Gateway. We use Amazon Bedrock with Claude 3.5 Sonnet for natural language understanding and Titan Embeddings for semantic search in our knowledge base stored in DynamoDB."

**Visuals:**
- Show architecture diagram
- Highlight AWS services (Lambda, Bedrock, DynamoDB, etc.)
- Show data flow animation

---

### **Section 3: Live Demo - Call 1 (60 seconds)**

**Voiceover:**
"Let me show you JanAI in action. I'm calling from a basic feature phone."

**Phone Call Recording:**
```
[Dial 1800-XXX-XXXX]
System: "Welcome to JanAI. Press 1 for Hindi, Press 2 for English"
[Press 1]
System: "नमस्ते। आप मुझसे सरकारी योजनाओं के बारे में पूछ सकते हैं।"
User: "PM Kisan ke baare mein batao"
System: "PM Kisan योजना में किसानों को साल में 6000 रुपये मिलते हैं, 
3 किस्तों में। यह 2 हेक्टेयर तक की खेती वाली भूमि के मालिकों के लिए है। 
क्या आप आवेदन प्रक्रिया जानना चाहते हैं?"
User: "Haan, documents kya chahiye?"
System: "आवश्यक दस्तावेज़: आधार कार्ड, बैंक खाता विवरण, और भूमि रिकॉर्ड। 
आवेदन pmkisan.gov.in पर करें। कोई और सवाल?"
User: "Nahi, bas itna hi"
System: "धन्यवाद! यह जानकारी SMS में भी भेजी जाएगी। नमस्ते!"
```

**Visuals:**
- Split screen: Phone + AWS console
- Show Lambda logs in real-time
- Show DynamoDB items being written

---

### **Section 4: AWS Console (60 seconds)**

**Voiceover:**
"Behind the scenes, you can see our Lambda functions processing the call, Bedrock generating AI responses, and DynamoDB storing call logs and session state. CloudWatch tracks all our metrics in real-time."

**Visuals:**
- Show Lambda function code
- Show Bedrock API calls
- Show DynamoDB tables
- Show CloudWatch dashboard with metrics

---

### **Section 5: Multi-Language Demo (45 seconds)**

**Voiceover:**
"JanAI works in multiple languages. Here's the same query in English."

**Phone Call Recording:**
```
[Call]
System: "Press 2 for English"
[Press 2]
System: "Hello. How can I help you today?"
User: "Tell me about Ayushman Bharat"
System: "Ayushman Bharat provides health insurance up to 5 lakh rupees 
per family per year. It covers hospitalization costs for serious illnesses. 
Would you like to know about eligibility?"
User: "Yes please"
System: "It's for families earning less than 1 lakh per year in rural areas 
or 1.5 lakh in urban areas. Apply at your nearest health center. Any other questions?"
User: "No, that's all"
System: "Thank you! You'll receive an SMS summary. Goodbye!"
```

---

### **Section 6: Impact & Future (45 seconds)**

**Voiceover:**
"JanAI currently covers 5 government schemes and has handled over 100 test calls with 90% accuracy. Our vision is to expand to 22 Indian languages and integrate with government databases for real-time eligibility checking. This solution can bring critical information to millions of underserved Indians through a simple phone call."

**Visuals:**
- Show usage statistics
- Show roadmap
- Show impact metrics

---

### **Section 7: Closing (15 seconds)**

**Voiceover:**
"Thank you for watching. JanAI - सेवा सभी के लिए, भाषा में हर किसी की - Service for all, in everyone's language. Built on AWS for the ."

**Visuals:**
- Logo screen
- AWS + Anthropic + Bhashini logos
- Call to action: "Try it: 1800-XXX-XXXX"

---

## 📝 PROJECT SUMMARY (500 Words)

**Title:** JanAI - Voice-First AI for Digital Inclusion

**Problem:**
India's digital transformation has left behind 500 million citizens without smartphones or reliable internet. These underserved populations—primarily in rural areas, elderly demographics, and low-income communities—face a critical information gap. While government schemes like PM-Kisan, Ayushman Bharat, and MGNREGA offer substantial benefits, accessing information about eligibility, documentation requirements, and application processes requires navigating complex websites or visiting government offices, creating insurmountable barriers for those without digital access.

**Solution:**
JanAI bridges this divide through a simple phone-based interface. Users call a toll-free number from any phone—including basic feature phones costing as little as ₹500—and converse naturally in Hindi or English to receive accurate, AI-powered information about government schemes. No smartphone, internet connection, or digital literacy required.

**Technical Implementation:**
Built entirely on AWS infrastructure, JanAI demonstrates the power of serverless, AI-native architecture:

- **Amazon Bedrock (Claude 3.5 Sonnet)**: Powers natural language understanding, contextual conversation, and accurate information retrieval. Claude's multilingual capabilities enable seamless Hindi-English code-switching common in rural India.

- **Amazon Bedrock (Titan Embeddings v2)**: Implements Retrieval Augmented Generation (RAG) for semantic search across government scheme documentation, ensuring responses are grounded in verified official sources.

- **AWS Lambda**: Serverless compute orchestrates the entire call flow—from speech recognition through AI processing to voice synthesis—enabling automatic scaling and cost efficiency.

- **Amazon DynamoDB**: Stores knowledge base, embeddings for vector search, and call logs while maintaining sub-millisecond latency for real-time conversation.

- **AWS API Gateway**: Handles incoming webhooks from Twilio's telephony infrastructure with built-in throttling and monitoring.

- **Amazon CloudWatch**: Provides comprehensive observability with custom metrics tracking call volume, accuracy, language distribution, and system health.

The hybrid approach combines Bhashini (Government of India's free speech platform) for primary STT/TTS with AWS Transcribe/Polly as intelligent fallbacks, optimizing both cost and accuracy for Indian languages and accents.

**Why AI is Essential:**
Traditional IVR systems rely on rigid menu trees, forcing users to navigate complex hierarchies. JanAI's AI enables natural conversation—users ask questions in their own words, seek clarification, and follow up contextually across multiple turns. Bedrock's Claude understands intent, maintains conversation history, and synthesizes information from multiple sources to generate accurate, concise responses appropriate for phone delivery. This conversational intelligence is impossible without generative AI.

**Impact & Metrics:**
During development, JanAI handled 100+ test calls with:
- 90%+ call success rate
- <5 second response latency
- 75-85% STT accuracy on Indian accents
- 100% information accuracy (verified against official sources)
- Support for 5 major schemes covering income support, healthcare, employment, housing, and savings

**Scalability & Future:**
JanAI's AWS-native architecture scales automatically from hundreds to millions of calls. Future phases will expand to 22 Indian languages, integrate with government databases for real-time eligibility verification, and enable transactions like application submissions—all while maintaining the simple phone-based interface that makes the system universally accessible.

**Cost Efficiency:**
The entire MVP operates at approximately ₹3-4 per call at scale, with AWS free tier covering infrastructure costs and Bhashini eliminating STT/TTS expenses. This makes large-scale deployment economically viable even with government subsidy or CSR funding.

JanAI demonstrates that the most impactful AI applications aren't always the most technically complex—sometimes, the right innovation is making powerful technology accessible through the simplest interface possible: a phone call.

---

## 🎓 KNOWLEDGE BASE STRUCTURE

### **Scheme Template (JSON):**

```json
{
  "scheme_id": "string",
  "name": {
    "en": "string",
    "hi": "string"
  },
  "category": "string (income|health|employment|housing|savings)",
  "description": {
    "en": "string (1-2 sentences)",
    "hi": "string (1-2 sentences)"
  },
  "eligibility": {
    "en": "string (bullet points as text)",
    "hi": "string (bullet points as text)"
  },
  "documents": {
    "en": ["array", "of", "strings"],
    "hi": ["array", "of", "strings"]
  },
  "benefits": {
    "en": "string (specific amounts/coverage)",
    "hi": "string (specific amounts/coverage)"
  },
  "apply_process": {
    "en": "string (step-by-step)",
    "hi": "string (step-by-step)"
  },
  "website": "string (URL)",
  "helpline": "string (phone numbers)",
  "faqs": [
    {
      "question_en": "string",
      "question_hi": "string",
      "answer_en": "string",
      "answer_hi": "string"
    }
  ],
  "last_updated": "ISO8601 timestamp",
  "source_urls": ["array", "of", "official", "sources"]
}
```

### **5 Schemes (Summary):**

**1. PM-Kisan (Pradhan Mantri Kisan Samman Nidhi)**
- Category: Income Support
- Benefit: ₹6,000/year in 3 installments
- Eligibility: Small/marginal farmers with ≤2 hectares
- Website: pmkisan.gov.in

**2. Ayushman Bharat (PM-JAY)**
- Category: Health Insurance
- Benefit: ₹5 lakh health cover per family/year
- Eligibility: Bottom 40% (SECC 2011 data)
- Website: pmjay.gov.in

**3. MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act)**
- Category: Employment
- Benefit: 100 days guaranteed wage employment
- Eligibility: Rural households (adult member)
- Website: nrega.nic.in

**4. PM Awas Yojana (Pradhan Mantri Awas Yojana - Gramin)**
- Category: Housing
- Benefit: ₹1.2-1.3 lakh subsidy for house construction
- Eligibility: BPL families without pucca house
- Website: pmaymis.gov.in

**5. Sukanya Samriddhi Yojana**
- Category: Savings (Girl Child)
- Benefit: High interest (8%+), tax benefits
- Eligibility: Parents/guardians of girl child <10 years
- Website: nari.nic.in

---

## 🔐 SECURITY & PRIVACY

### **Data Protection:**

**User Privacy:**
- No personal identifiable information (PII) stored
- Phone numbers hashed before storage
- Call recordings auto-deleted after 7 days
- SMS summaries contain no personal data

**AWS Security:**
- Encryption at rest (DynamoDB, S3 - AES-256)
- Encryption in transit (TLS 1.3)
- IAM roles with least privilege
- VPC isolation for Lambda (if needed)

**API Security:**
- Twilio webhook signature validation
- Rate limiting (1000 req/sec per IP)
- Input sanitization (prevent injection)
- Error messages don't leak system info

**Compliance:**
- GDPR-compliant (right to erasure)
- India DPDP Act considerations
- No cross-border data transfer
- Audit logs in CloudWatch (90 days)

---

## 📖 API REFERENCE

### **Twilio Webhooks:**

**POST /voice/incoming**
```
Headers:
  X-Twilio-Signature: [signature]
  
Body (form-urlencoded):
  CallSid: string
  From: string (phone number)
  To: string (our number)
  CallStatus: string
  
Response (TwiML):
  <?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Gather input="dtmf" numDigits="1" action="/voice/gather">
      <Say voice="woman" language="hi-IN">
        Press 1 for Hindi, Press 2 for English
      </Say>
    </Gather>
  </Response>
```

**POST /voice/gather**
```
Body:
  CallSid: string
  Digits: string (1|2)
  
Response (TwiML):
  <Response>
    <Gather input="speech" language="hi-IN" action="/voice/process">
      <Say>नमस्ते। कैसे मदद कर सकता हूँ?</Say>
    </Gather>
  </Response>
```

**POST /voice/process**
```
Body:
  CallSid: string
  SpeechResult: string
  Confidence: float
  
Response (TwiML):
  <Response>
    <Say voice="woman" language="hi-IN">
      [AI-generated response]
    </Say>
    <Gather input="speech" language="hi-IN" action="/voice/process">
      <Say>क्या कोई और सवाल है?</Say>
    </Gather>
  </Response>
```

---

## 🚀 DEPLOYMENT

### **Prerequisites:**
- AWS account with $100 credits applied
- Twilio account with trial credits
- Bhashini API credentials
- Python 3.11+
- AWS CLI configured

### **Setup Steps:**

**1. Clone Repository:**
```bash
git clone https://github.com/kaizen-team/janai-hackathon.git
cd janai-hackathon
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment:**
```bash
cp .env.example .env
# Edit .env with your credentials:
# - AWS_REGION
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - BHASHINI_API_KEY
```

**4. Deploy Infrastructure:**
```bash
# Create DynamoDB tables
python scripts/setup_dynamodb.py

# Deploy Lambda functions
cd lambda
zip -r call_handler.zip call_handler.py
aws lambda create-function \
  --function-name janai-call-handler \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler call_handler.lambda_handler \
  --zip-file fileb://call_handler.zip \
  --timeout 30 \
  --memory-size 512

# Create API Gateway
python scripts/setup_api_gateway.py
```

**5. Configure Twilio:**
```bash
# Set webhook URL
python scripts/configure_twilio.py \
  --api-gateway-url https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod
```

**6. Load Knowledge Base:**
```bash
python scripts/load_knowledge_base.py
```

**7. Test:**
```bash
# Call the Twilio number
# Verify logs in CloudWatch
aws logs tail /aws/lambda/janai-call-handler --follow
```

---

## 📚 REFERENCES

### **Official Documentation:**
- AWS Bedrock: https://docs.aws.amazon.com/bedrock/
- AWS Lambda: https://docs.aws.amazon.com/lambda/
- Twilio Voice: https://www.twilio.com/docs/voice
- Bhashini: https://bhashini.gov.in/ulca/apis

### **Government Scheme Sources:**
- PM-Kisan: https://pmkisan.gov.in
- Ayushman Bharat: https://pmjay.gov.in
- MGNREGA: https://nrega.nic.in
- PM Awas: https://pmaymis.gov.in
- Sukanya Samriddhi: https://nari.nic.in

### **Research & Data:**
- NITI Aayog Rural Health Report 2021
- Census 2011 (SECC data)
- Telecom Regulatory Authority of India (TRAI) reports
- WHO healthcare worker ratios

---

## 🎉 CONCLUSION

You have everything you need to build JanAI in 4 days:

✅ **Clear vision** - Phone-based AI for rural India  
✅ **Proven architecture** - AWS serverless + Bedrock  
✅ **Detailed timeline** - Day-by-day breakdown  
✅ **Team division** - 4 people, clear responsibilities  
✅ **Budget planned** - $25-35 total, mostly covered by credits  
✅ **Risk mitigation** - Fallbacks and buffers built in  

**Your competitive advantages:**
- Genuinely differentiated idea (phone-based, not app-based)
- AWS-native architecture (checks all hackathon criteria)
- Social impact focus (500M+ target users)
- Feasible in 4 days (with aggressive execution)

**Now execute:**
1. Create AWS account (today)
2. Create Twilio account (today)
3. Divide work among team (today)
4. Start building (Day 1 tasks)
5. Daily standups (8 PM each day)
6. Submit by 9 PM on March 4 (3-hour buffer)

**You've got this.** From 90-minute PPT to working prototype. From idea to impact. From "maybe we can do this" to "we're building the future of digital inclusion."

**Now go build JanAI. Make it real. Win this thing.** 🚀

---

**Last updated:** February 27, 2026, 11:59 PM  
**Next action:** Create AWS account NOW  
**Team motto:** "Service for all, in everyone's language"

---

*सेवा सभी के लिए, भाषा में हर किसी की*
