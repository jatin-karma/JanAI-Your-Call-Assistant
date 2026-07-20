# JanAI

**Voice-First AI for Digital Inclusion**

JanAI is a voice-first AI platform designed to bridge India's digital divide by providing multilingual, low-latency, voice-accessible digital services to 500M+ citizens who are excluded from traditional smartphone apps.

---

## 🎯 Problem Statement

Over 500 million Indians are excluded from digital services due to:
- Lack of smartphone access or high-speed data
- Limited digital & textual literacy
- Regional language and dialect barriers
- Complex text-based government portals

## 💡 Solution

JanAI provides a ultra-low latency voice-based interface accessible via basic feature phones or web browsers, enabling users to access critical government schemes, healthcare advice, and agricultural market prices in their native spoken language.

---

## ✨ Key Features

### 1. **Multi-Domain Information Access**
- Government schemes & eligibility rules (PM Kisan, Ayushman Bharat, Ladli Behna, etc.)
- Healthcare guidance & public health awareness
- Agricultural mandi prices & crop advisories
- Civic services and document requirements

### 2. **Multilingual Voice & Dynamic Switching**
- Supports Hindi (`hi`), English (`en`), Marathi (`mr`), and Tamil (`ta`)
- Automatic script-density & phonetic language detection
- Mid-call dynamic language switching (e.g. *"explain in english"*)

### 3. **Ultra-Low Latency (<600ms Turnaround)**
- **Cartesia Sonic-3 Integration:** Instant **40ms TTFA** (Time-to-First-Audio) voice synthesis for English and Hindi/Hinglish
- **3-Layer RAG Bypass:** Skips heavy vector database lookups for simple greetings and casual conversational turns

### 4. **WebRTC Hardware DSP & Noise Suppression**
- Built-in WebRTC acoustic echo cancellation, background noise suppression, and auto-gain control (`16kHz Mono`)
- Crystal clear speech recognition even in high-noise environments

### 5. **Privacy & Production Security**
- Serverless AWS Lambda execution environment with isolated call containers
- Hardened security configuration preventing credential exposure
- Secure pre-signed S3 audio transport

---

## 🚀 How It Works

1. **Call JanAI** — User dials the PSTN phone number or starts WebRTC call on the website.
2. **Auto-Detect Language** — The system evaluates spoken phonemes or script density.
3. **Ask Question** — Speak naturally in Hindi, English, Marathi, or Tamil.
4. **AI Responds** — Sub-second voice reply generated using Cartesia Sonic-3 / Sarvam AI.
5. **Multi-Turn Follow-Up** — Active topic tracking maintains context across questions.

**Average Call Turn Latency:** < 600ms  
**Cost per Call Minute:** ₹2.00 (85% saving vs traditional human call centers)

---

## ⚠️ Telephony & Access Notes

- **Inbound PSTN Access:** Inbound calls route directly via Twilio SIP Trunks to AWS Lambda API Gateway.
- **WebRTC Browser Agent:** Full WebRTC browser agent available on live deployment (`https://janai-beta.vercel.app`).

---

## 🏗️ Architecture

### System Components

**User Interface Layer:**
- Twilio Voice API (telephony PSTN)
- WebRTC Audio DSP Helper (`audioConstraints.js`)
- React Frontend Widget (`website/`)

**Processing & Services Layer (Modular OOP):**
- AWS Lambda (`janai-call-handler`)
- `VoiceSynthesizer` service — Cartesia Sonic-3 (Primary 40ms) & Sarvam Bulbul v2 (Regional)
- `SpeechRecognizer` service — Sarvam Saarika STT + Twilio Gather with Devanagari script density classifier
- `LanguageManager` service — Mid-call explicit switch detection

**Intelligence Layer:**
- Amazon Bedrock Nova Lite (`amazon.nova-lite-v1:0`)
- Titan Text Embeddings v2 (`amazon.titan-embed-text-v2:0`)
- 3-Layer RAG Pre-Filter Engine

**Data Layer:**
- AWS S3 (`janai-documents-2026`) — Presigned audio playback
- Amazon DynamoDB (`janai_calls`, `janai_vectors`, `janai_phone_profiles`)

---

## 🛠️ Technology Stack

### Telephony & WebRTC
- Twilio Voice SDK
- WebRTC Audio Constraints (Echo Cancellation, Noise Suppression, Auto Gain Control)

### Speech Processing
- **TTS (Primary 40ms):** Cartesia Sonic-3
- **TTS (Regional):** Sarvam AI Bulbul v2 (Hindi, Marathi, Tamil)
- **TTS (Fallback):** Amazon Polly
- **STT:** Sarvam Saarika v1 + Twilio Native Gather with Devanagari script classifier

### AI & Cloud Compute
- AWS Bedrock (Nova Lite)
- AWS Lambda (Python 3.11 Serverless)
- AWS DynamoDB (Vector & Conversation Storage)
- AWS S3 (Multi-part deployment & audio host)

---

## 💰 Economics & Cost Optimization

### Unit Cost Breakdown (per Call Minute)

| Component | Cost per Min | % of Total |
|---|---|---|
| **Twilio PSTN Transport** | ₹1.08 | 54.0% |
| **Cartesia Sonic-3 TTS** | ₹0.35 | 17.5% |
| **AWS Bedrock LLM** | ₹0.22 | 11.0% |
| **Sarvam Saarika STT** | ₹0.15 | 7.5% |
| **AWS DynamoDB & S3** | ₹0.20 | 10.0% |
| **TOTAL COST / MINUTE** | **₹2.00** | **100%** |

* **Human Call Center Cost:** ₹15.00 / minute
* **JanAI Cost:** **₹2.00 / minute** (**85% Cost Reduction**)

---

## 📊 Roadmap & Deployment

- ✅ **Phase 1:** Multi-language voice agent (Hindi, English, Marathi, Tamil)
- ✅ **Phase 2:** Cartesia Sonic-3 40ms TTFA integration & 3-layer RAG bypass
- ✅ **Phase 3:** WebRTC DSP noise suppression & modular OOP code architecture
- ✅ **Phase 4:** Production S3 multi-part deployment pipeline (`scripts/deploy.ps1`)

- SMS integration

**Phase 3 (Months 7-12):** Scale & Optimize
- 1M+ users
- Regional partnerships
- Cost optimization
- Advanced AI features

**Phase 4 (Year 2+):** National Rollout
- 100M+ users
- All major Indian languages
- Government integration
- Pan-India coverage

---

## 🎯 Why JanAI?

### Unique Value Proposition

| Feature | JanAI | Traditional Apps | IVR Systems |
|---------|-----------|------------------|-------------|
| **No smartphone needed** | ✅ | ❌ | ✅ |
| **AI-powered intelligence** | ✅ | ✅ | ❌ |
| **Natural conversation** | ✅ | ❌ | ❌ |
| **Multi-language support** | ✅ (8+) | Limited | Limited |
| **No internet required** | ✅ | ❌ | ✅ |
| **Cost effective** | ✅ (₹4) | Free* | ₹15-50 |
| **Accessibility** | 100% | 40% | 70% |

---

## 🌍 Alignment with UN SDGs

JanAI directly contributes to:
- **SDG 1:** No Poverty - Access to government schemes
- **SDG 3:** Good Health - Healthcare information
- **SDG 4:** Quality Education - Knowledge access
- **SDG 10:** Reduced Inequalities - Digital inclusion

---

## 🚀 Getting Started

### Prerequisites
- AWS Account with Bedrock model access enabled
- Twilio Account with Voice API access
- Sarvam AI API key (for Hindi TTS)
- AWS DynamoDB tables and S3 bucket provisioned

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/janai.git
cd janai

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and configuration

# Deploy to AWS
aws cloudformation deploy --template-file infrastructure/template.yaml

# Set up Twilio webhook
# Point Twilio Voice URL to your Lambda function endpoint
```

### Configuration

Edit `.env` file:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number
SARVAM_API_KEY=your_sarvam_api_key
BEDROCK_MODEL_ID=us.anthropic.claude-3-5-haiku-20241022-v1:0
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
DYNAMODB_CALLS_TABLE=janai-calls
DYNAMODB_KNOWLEDGE_TABLE=janai-knowledge
DYNAMODB_VECTORS_TABLE=janai-vectors
S3_DOCUMENTS_BUCKET=janai-documents
AWS_REGION=us-east-1
```

---

## 📱 Demo

**Call the JanAI Demo Line:** 1800-XXX-XXXX

Try asking:
- "Mujhe kisan yojana ke baare mein bataye" (Tell me about farmer schemes)
- "What are the COVID vaccination centers near me?"
- "Ration card kaise banaye?" (How to make a ration card?)

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Areas for Contribution
- Additional language support
- Domain-specific knowledge bases
- UI/UX improvements
- Performance optimization
- Documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Team Kaizen**

**Team Lead:** Jatin Karma

**Team Members:**
- Divya Verma
- Deepesh Patel
- Devansh Burman

---

## 🙏 Acknowledgments

- **AWS & Anthropic** -  organizers
- **Sarvam AI** - Hindi text-to-speech
- **Twilio** - Telephony infrastructure and speech recognition
- **Amazon Polly** - Fallback TTS

---


**Join us in bridging India's digital divide!**

*"सभी के लिए डिजिटल सेवाएं - JanAI"*  
*(Digital Services for All - JanAI)*
