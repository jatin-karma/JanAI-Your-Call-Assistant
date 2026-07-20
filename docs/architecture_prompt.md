# Architecture Diagram Generation Prompt

This file contains the prompt and code to generate the architecture diagram for JanAI. You can copy and paste the prompt below into any AI diagramming tool (like **Eraser.io**, **Mermaid Live Editor**, or **ChatGPT/Claude**) to generate a clean, professional architecture diagram.

---

## 🎨 Option 1: Mermaid.js Code (Copy-paste directly to [Mermaid Live Editor](https://mermaid.live))

```mermaid
graph TD
    %% Styling
    classDef ui fill:#FFE5B4,stroke:#D2B48C,stroke-width:2px;
    classDef gate fill:#E6F2FF,stroke:#8FA9C4,stroke-width:2px;
    classDef lambda fill:#FFE6E6,stroke:#D98880,stroke-width:2px;
    classDef ai fill:#E6F9E6,stroke:#82C482,stroke-width:2px;
    classDef db fill:#F3E6FF,stroke:#A385C2,stroke-width:2px;

    %% User Layer
    subgraph UI ["User Access Channels"]
        PhoneUser["📞 Phone Caller (Telephony)"]:::ui
        WebUser["💻 Web Interface (Browser WebRTC)"]:::ui
    end

    %% Entry Gateways
    subgraph Gateway ["Ingress & Gateways"]
        TwilioVoice["Twilio Voice API<br>(Inbound / Outbound Calls)"]:::gate
        APIGateway["AWS API Gateway<br>(REST Endpoints)"]:::gate
    end

    %% Orchestration Layer
    subgraph Compute ["Serverless Compute (AWS Lambda)"]
        CallInitiator["janai-call-initiator<br>(Triggers callbacks)"]:::lambda
        CallHandler["janai-call-handler<br>(TwiML IVR & Call Orchestrator)"]:::lambda
        WebAgent["janai-web-agent<br>(3D Avatar Chat Hub)"]:::lambda
    end

    %% AI Integration Layer
    subgraph AI ["AI Services Layer"]
        LLM["Amazon Bedrock (Nova Lite)<br>(RAG, Eligibility, Reasoning)"]:::ai
        TTS["Sarvam AI / Cartesia / Polly<br>(Text-to-Speech Audio Gen)"]:::ai
        STT["Twilio Gather / Sarvam STT<br>(Speech-to-Text Transcription)"]:::ai
    end

    %% Database & S3
    subgraph Storage ["Data & Storage Layer"]
        DDB_Calls["DynamoDB: janai_calls<br>(Session Memory & Logs)"]:::db
        DDB_KB["DynamoDB: janai_knowledge<br>(RAG Scheme Database)"]:::db
        S3Bucket["AWS S3 Bucket<br>(Docs & Cached TTS WAVs)"]:::db
    end

    %% Flow Connections
    PhoneUser <-->|Dial / Call Back| TwilioVoice
    WebUser <-->|API Requests / WebRTC| APIGateway
    
    TwilioVoice <-->|TwiML Webhooks| CallHandler
    APIGateway <-->|HTTP POST| CallInitiator
    APIGateway <-->|HTTP Chat / STT| WebAgent
    
    CallInitiator -->|Trigger Outbound Call| TwilioVoice

    %% Compute Connections to AI
    CallHandler <-->|1. Transcribe Voice| STT
    CallHandler <-->|2. Fetch Answer| LLM
    CallHandler <-->|3. Generate Audio| TTS
    
    WebAgent <-->|Fetch Web Response| LLM
    WebAgent <-->|Generate Web Voice| TTS

    %% Compute Connections to Storage
    CallHandler <-->|Read/Write Call History| DDB_Calls
    CallHandler <-->|Query Scheme Context| DDB_KB
    TTS -->|Cache Audio Files| S3Bucket
    CallHandler -->|Fetch Cached Audio URL| S3Bucket
```

---

## ✍️ Option 2: AI Tool Text Prompt (Copy-paste into **Eraser.io** or **ChatGPT**)

```text
Generate a clean, high-level architecture diagram for a voice-powered AI system named "JanAI".

Use a professional, modern layout (left-to-right or top-to-bottom flow) with standard component shapes and harmonious pastel colors. Group the components into 4 distinct layers:

1. ACCESS LAYER (User Channels):
   - "Phone Caller (Cellular / Telephony)"
   - "Web Browser (Live WebRTC Audio & Chat Widget)"

2. GATEWAY & INGRESS:
   - "Twilio Voice API" (Handles cellular inbound/outbound connection)
   - "AWS API Gateway" (Handles REST endpoint routing and Web CORS)

3. ORCHESTRATION LAYER (Serverless Compute):
   - "AWS Lambda: janai-call-initiator" (Triggers outbound callback calls)
   - "AWS Lambda: janai-call-handler" (Main orchestrator processing incoming calls, TwiML IVR, and responses)
   - "AWS Lambda: janai-web-agent" (Handles web-centric avatar conversation & web STT/TTS)

4. COGNITIVE & DATA LAYER:
   - "STT (Twilio Native / Sarvam AI)"
   - "LLM (Amazon Bedrock Nova Lite / OpenAI fallback)"
   - "TTS (Sarvam AI / Cartesia / Polly fallback)"
   - "Amazon DynamoDB" (Stores call history and RAG knowledge vectors)
   - "Amazon S3" (Stores source docs and cached speech audio wavs)

Ensure the connections show:
- Inbound/Outbound cellular connections routing through Twilio Voice API.
- Web browser calling AWS API Gateway.
- The Call Handler Lambda orchestrating STT translation -> querying LLM -> synthesizing TTS audio -> returning TwiML response.
- Read/Write operations from Lambdas to DynamoDB and S3 for persistence and caching.

Keep it simple, avoid overlapping lines, and make it easy to understand for developers and stakeholders.
```
