# 💼 JanAI — Business, Revenue & Cost Management Architecture

This document provides a comprehensive analysis of the **Business Model, Monetization Strategies, Unit Economics, and Server/API Cost Reduction Strategies** for **JanAI**.

---

## 1. 📊 Per-Turn Unit Economics & Cost Breakdown

The following table breaks down the raw technology cost for a **1-minute conversational voice turn** (approx. 4 conversation exchanges) on JanAI:

| Infrastructure Component | Provider | Unit Metric | Cost per Min / Turn | % of Total Cost |
|---|---|---|---|---|
| **Telephony / Transport** | Twilio PSTN | $0.0130 / min | ₹1.08 / min | **54.0%** |
| **LLM Inference** | AWS Bedrock (Nova-Lite) | $0.00006 / 1K tokens | ₹0.22 / min | **11.0%** |
| **Speech-to-Text (STT)** | Sarvam Saarika v1 | ₹0.15 / min | ₹0.15 / min | **7.5%** |
| **Text-to-Speech (TTS)** | Cartesia Sonic-3 | $0.0005 / turn | ₹0.35 / min | **17.5%** |
| **Database & Vector RAG** | AWS DynamoDB & Titan | Pay-per-request | ₹0.10 / min | **5.0%** |
| **Cloud Storage** | AWS S3 Bucket | $0.023 / GB | ₹0.10 / min | **5.0%** |
| **TOTAL COST PER CALL MINUTE** | — | — | **₹2.00 / min** (~$0.024) | **100%** |

> **Comparative Industry Benchmark:** A traditional human agent call center in India costs **₹12.00 – ₹18.00 per minute**. JanAI reduces citizen helpline operational costs by **85% – 88%**.

---

## 2. ⚡ Server & API Architecture Cost Reduction Strategy

To scale JanAI to millions of rural citizens while maintaining low operational overhead, we implement a **4-tier Cost Optimization Architecture**:

```
                       ┌────────────────────────────────────────┐
                       │   SERVERLESS COST REDUCTION STACK      │
                       └────────────────────────────────────────┘
                                            │
   ┌────────────────────────────────────────┴────────────────────────────────────────┐
   │                                                                                 │
   ▼                                                                                 ▼
[1. Server Response Caching]                                       [2. Indian PSTN Trunking]
Skips LLM for repeated scheme/mandi queries                       Switch Twilio → Exotel / Agora
Cuts LLM token costs by 75%                                       Cuts telephony transport costs by 70%
   │                                                                                 │
   ▼                                                                                 ▼
[3. 3-Layer RAG Bypass]                                            [4. Bedrock Nova-Lite Batching]
Bypasses vector DB for simple chat/greetings                      Uses lightweight Nova-Lite vs expensive Claude
Cuts DynamoDB RCU costs by 60%                                    Cuts LLM generation cost by 90%
```

### Strategy Breakdown:
1. **Server Response Caching (Option B):** 
   * Caches answers for frequent queries (e.g. *"PM Kisan eligibility"*) in DynamoDB `janai_cache`. Repeated queries return cached answers in **<20ms for $0.00 LLM cost**.
2. **Indian PSTN & WebRTC Trunking (Exotel / Agora):** 
   * Replacing international Twilio routes with domestic Indian SIP trunks (Exotel / Tata Tele / Agora) drops call transport costs from **₹1.08/min down to ₹0.30/min**.
3. **Bedrock Nova-Lite vs Claude 3.5 Sonnet:** 
   * Using Amazon Nova-Lite (`amazon.nova-lite-v1:0`) provides 95% of the intelligence of top-tier models at **1/15th of the cost**.

---

## 3. 💵 Revenue & Monetization Model

JanAI operates a **Hybrid B2G, B2B, and Freemium SaaS Model**:

```
                               ┌─────────────────────────┐
                               │   JANAI REVENUE MODEL   │
                               └───────────┬─────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
   [1. B2G Licensing]             [2. B2B Agribusiness]            [3. B2C Freemium Web]
 State Govt Helplines            Enterprise Advisory API          Free 10 mins/month
 ₹5–10 Lakhs/month/state         ₹1.50/API query                  ₹99/month Unlimited
```

### A. B2G (Business-to-Government) State Helpline Subscriptions
* **Target:** State Departments of Agriculture, Public Health (NHM), and Rural Development.
* **Pricing Model:** Annual SaaS Contract (₹50 Lakhs – ₹1 Crore / year per state).
* **Value Proposition:** Replaces overwhelmed government landline helplines with a 24/7 AI voice bot capable of handling 50,000 concurrent calls during crop damage or disaster events.

### B. B2B Enterprise Agribusiness & CSR Partnerships
* **Target:** Fertilizer manufacturers (IFFCO, Coromandel), seed suppliers, and microfinance institutions (NABARD, regional banks).
* **Pricing Model:** Pay-per-query API integration (₹1.50 per voice advisory interaction).
* **Value Proposition:** Agri-companies embed JanAI into their dealer networks to provide localized soil, crop disease, and market price advice.

### C. B2C Consumer Freemium (Web & App)
* **Free Tier:** 10 free voice minutes per month per verified phone number.
* **Premium Tier (JanAI Plus):** ₹99 / month for unlimited voice search, personalized scheme application tracking, and priority call line access.

---

## 📈 Financial Projections (100,000 Monthly Active Users)

* **Monthly Active Calls:** 500,000 call minutes
* **Gross Infrastructure Cost (Optimized):** 500,000 mins × ₹0.80/min = **₹4,00,000 / month**
* **Projected Monthly Revenue (B2G + B2B):** **₹25,00,000 / month**
* **Projected Net Gross Margin:** **84%**
