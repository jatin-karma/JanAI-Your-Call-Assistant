# JanAI — PPT Creation Guide for Team Kaizen
## 

> **Who this file is for:** Your teammates who are building the final presentation.
> Three tools, three tasks — do them in order.

---

## ⚡ QUICK FACTS (before you start, know these cold)

| | |
|---|---|
| **Product** | JanAI — वाणीसेवा ("Voice Service") |
| **Live number** | +1 831 298 8145 |
| **Problem** | 440M+ Indians have a phone but can't access AI (no smartphone, no internet, no English) |
| **Solution** | Call a number. Speak Hindi/Marathi/Tamil/English. AI answers in under 4 seconds. |
| **Team** | Team Kaizen — jatin karma + 3 members |
| **Track** |  2026 —  (Voice AI for Rural India) |
| **Tech** | Twilio → AWS Lambda → Amazon Bedrock Nova Lite → Sarvam AI TTS |
| **Real demo** | Yes. The phone number works RIGHT NOW. |
| **Cost at scale** | ₹4 per call (₹12.50 current) |

---

---

# TASK 1 — GAMMA.APP BASE PRESENTATION

## Instructions for teammate
1. Go to [gamma.app](https://gamma.app)
2. Click **"Create new"** → **"Paste in text"**
3. Copy **everything between the `===GAMMA START===` and `===GAMMA END===` tags** below
4. Paste it into Gamma's text input
5. Choose theme: **"Dark"** or **"Bold"** — avoid clean/minimal whites, this is an impact story
6. Let Gamma generate, then export as PowerPoint (.pptx)
7. Hand the .pptx file to the next teammate (Task 2 — Slides Pilot)

---

===GAMMA START===

# JanAI — वाणीसेवा
## India's Knowledge. Now in Every Voice.
###  | Team Kaizen

---

# The Problem

440 million Indians have a basic mobile phone.

They cannot access:
- Government scheme money they are already entitled to
- Health guidance during a medical emergency
- Crop market prices before they sell their harvest
- Legal rights when they are being exploited

**Not because AI doesn't exist.**
**Because every AI requires a smartphone, internet, and English.**

The digital divide is not a lack of phones.
It is a wall built from apps, data plans, and one language.

---

# One Number Changes Everything

**Dial +1 831 298 8145**

No app. No data. No internet. No English required.

Just speak.

In Hindi. In Marathi. In Tamil. In English.

In under 4 seconds, an AI answers back — in your language, in your voice, with verified information.

This is JanAI.

---

# Who We're Building For

**The farmer in Vidarbha** who doesn't know today's wheat price at the mandi.

**The mother in Jharkhand** who doesn't know if her family qualifies for Ayushman Bharat.

**The migrant worker in Surat** who was cheated of wages and doesn't know his legal rights.

**The elderly man in Tamil Nadu** who is too proud to ask his children for help again.

They all have one thing in common:
They have a phone. That's all they need.

---

# How JanAI Works

**Step 1.** User dials from any phone — keypad phone, smartphone, anything

**Step 2.** Speaks naturally in their language — no menus, no commands

**Step 3.** AI listens, understands, retrieves verified knowledge, responds

**Step 4.** Answer delivered as voice in under 4 seconds

**Step 5.** Follow-up naturally — the AI remembers the whole conversation

No literacy needed. No internet needed. Just a voice.

---

# Meet the AI Agents

JanAI has three distinct AI personalities — each an expert in their domain.

**Arya** — Warm and knowledgeable didi
Government schemes, legal rights, general knowledge, everyday help
Speaks: Hindi, Marathi, Tamil, English

**Hitesh** — Straight-talking farming expert
Mandi prices (live from 3,000+ markets), crop advice, PM-Kisan, Fasal Bima
Speaks: Hindi, Marathi, Tamil, English

**Vidya** — Gentle health friend
Ayushman Bharat, mental wellness, ASHA services, medical guidance, crisis support
Speaks: Hindi, Marathi, Tamil, English

Each agent has gender-accurate grammar, distinct personality, and routes instantly to the right expert based on what you ask.

---

# The Technology

**Voice Pipeline (real-time, under 4 seconds):**
Twilio (telephony + STT) → AWS API Gateway → AWS Lambda → Amazon Bedrock Nova Lite (LLM) → Sarvam AI bulbul:v2 (TTS) → Caller hears answer

**Knowledge Layer (Verified RAG):**
Amazon Titan Embeddings → DynamoDB Vector Search → 30+ government schemes, verified by human + AI review

**Live Data:**
data.gov.in mandi API — real-time crop prices from 3,000+ mandis

**Safety Layer:**
Crisis detection → iCall mental health referral (9152987821)
Verified helpline numbers for PM-Kisan, Ayushman Bharat, Women's helpline, Child helpline

**Fallback Architecture:**
Sarvam AI TTS → Amazon Polly fallback
Bedrock Nova Lite → OpenAI GPT-4o-mini fallback
Every critical path has redundancy

---

# Why This Is Hard (And Why It Works)

Most "voice AI" doesn't actually work at the bottom of the pyramid. Here's what everyone else skips:

**Latency.** Rural India runs on 2G. We optimized from 10 seconds to 3.6 seconds through parallel TTS, Bedrock streaming, and in-memory caching.

**Language.** Not just translation — Sarvam AI trained on Indian voices, Indian accents, Indian code-switching. Arya sounds like someone from Lucknow, not a Google TTS robot.

**Trust.** Every critical fact (helpline numbers, scheme eligibility, legal rights) is verified by AI review + human approval before it reaches a caller. A wrong helpline to someone in crisis is not acceptable.

**Access.** Works on a ₹500 keypad phone from 2007. PSTN network. No WiFi. No app. Nothing.

---

# Knowledge Base

JanAI has verified information on:

**Government Schemes:** PM-Kisan, Ayushman Bharat, MGNREGA, PM Awas Yojana, Sukanya Samriddhi, PM Ujjwala, Jan Dhan Yojana, PM Mudra Yojana, Atal Pension, Fasal Bima, SVANidhi, Scholarship schemes

**Health:** Ayushman Bharat eligibility, ASHA worker contacts, maternal health, mental wellness, iCall referral system

**Agriculture:** Live mandi prices (Agmarknet via data.gov.in), crop insurance, PM-Kisan status, soil health, weather guidance

**Legal & Civic:** Aadhaar, ration card, voter ID, land records, RTI, labour rights, women's rights

**Crisis Support:** 24/7 emotional support, mental health crisis detection, immediate referral to iCall (9152987821) and Vandrevala Foundation

---

# The Numbers

4 seconds — average response time

4 languages — Hindi, Marathi, Tamil, English

30+ government schemes — in the knowledge base

3,000+ mandis — live price coverage via data.gov.in

₹4 — cost per call at scale

500 million — Indians this can reach with a basic phone

0 — apps to download, data plans needed, English required

---

# The Road Ahead

**Phase 1 (Now):** Hindi, Marathi, Tamil, English — 4 languages, core domains working

**Phase 2 (3 months):** Telugu, Kannada, Bengali, Bhojpuri via Sarvam AI — targeting 8 languages. Bhashini integration (government-backed, 22 scheduled languages).

**Phase 3 (6 months):** B2B2C partnerships — ASHA workers, NGOs, Gram Panchayats, CSC operators using JanAI as infrastructure

**Phase 4 (12 months):** Government partnerships — state helplines, PM portal integration, subsidized toll-free rollout for BPL households

**Revenue:** Government contracts, NGO licensing, CSC operator model (₹1–2/call at volume)

---

# The Team

**Team Kaizen** — "Effort" in Hindi

We built this because we believe the AI revolution should not have a minimum device requirement.

India's next 440 million internet users won't come online through apps.
They'll come through their voice.

JanAI is ready for them.

**Dial +1 831 298 8145 — right now, live, in Hindi.**

Don't have international call balance? Visit **janai.me** — enter your number and we'll call you back. Free, instant, no app needed.

---

===GAMMA END===

---

---

# TASK 2 — SLIDES PILOT (nanobanana enhancement)

## Instructions for teammate
1. Take the `.pptx` file exported from Gamma (Task 1 output)
2. Go to [SlidePilot](https://slidespilot.com) (or wherever nanobanana is accessible)
3. Upload the Gamma PPT
4. Paste the prompt below into the SlidePilot creative direction box
5. Let it regenerate the presentation with full nanobanana power
6. Export final version

---

## SlidePilot / nanobanana Prompt

```
Redesign this JanAI presentation. KEEP ALL TEXT EXACTLY AS-IS.

GENERATE AI IMAGES for every slide — cinematic, painterly, Indian rural realism, warm tones.

Per-slide images:
- Cover: Indian village morning, golden light, woman on basic phone. Dark gradient left for text.
- Problem: One silhouette with keypad phone excluded from a digital crowd.
- Who We're Building For: Four portraits — Vidarbha farmer, Jharkhand mother, Surat migrant worker, elderly Tamil Nadu man.
- How It Works: Icon flow — phone → sound wave → AI brain → speaker. Warm amber on dark bg.
- AI Agents: Three avatar cards — Arya (gold/saree), Hitesh (earthy/field), Vidya (soft light/health).
- Knowledge Base: Illustrated collage — PM-Kisan form, Ayushman card, mandi price board.
- Technology: Glowing pipeline — Twilio → Lambda → Bedrock → Sarvam AI → caller's ear.
- Why It's Hard: 4 quadrants — 2G signal bars, Indian script, verified stamp, ₹500 Nokia.
- Road Ahead: Timeline ribbon, milestone illustrations, hopeful.
- Final CTA: Phone held up to light, gold tones. "+1 831 298 8145" displayed huge.

COLORS: Dark bg #0f0f0f–#1a1a1a. Accent #F0A832 saffron gold. Text warm white. No blues.

TYPOGRAPHY: Bold headers. Stats like "440 Million" and "3.6 seconds" oversized. Noto Sans Devanagari for Hindi text.

TRANSITIONS: Cross-dissolve only. No spin, no fly-in.

TONE: Direct, raw, human. Not a startup pitch — a product for people ignored by every other AI.
```

---

---

# TASK 3 — VIDEO SCRIPT (3–5 minute demo video)

## Instructions for teammate
This is the demo video for the hackathon submission. Shoot it in portrait or landscape — 1080p minimum. You need:
- One person on camera (the "host") — wearing something clean and simple
- A working phone (to make a real call)
- Screen recording of the website
- Subtitles (Hindi appears on screen when the AI speaks Hindi)

**Total target runtime: 3–4 minutes**

---

## VIDEO SCRIPT

---

**[00:00 – 00:20 — COLD OPEN]**
*[Screen black. Then cut to: a rural scene — farmer's hand, a basic phone. OR just cut straight to the host with phone in hand.]*

**HOST (to camera, direct, calm):**
"Four hundred million Indians have a phone. But every AI assistant requires a smartphone, an internet connection, and English.

JanAI changes that. Right now."

*[Host dials +1 831 298 8145 on their phone.]*

---

**[00:20 – 01:10 — LIVE DEMO — PHONE CALL]**
*[Show the phone screen — number dialing. Audio is ON.]*

**HOST (whispering to camera, while phone rings):**
"This is a live AI voice call. No app. No data. Just a phone number."

*[The call connects. The AI greets in Hindi: "वाणीसेवा में आपका स्वागत है, मैं आर्या हूँ। बताइए, आज मैं कैसे मदद करूँ?"]*

*[Subtitles appear: "Welcome to JanAI. I'm Arya. How can I help you today?"]*

**HOST (speaks into phone, in Hindi):**
"पीएम किसान में कितने पैसे मिलते हैं?"
*(Translation: "How much money does PM-Kisan give?")*

*[AI responds within 4 seconds. Subtitles appear.]*

*[HOST ends call.]*

**HOST (to camera):**
"Four seconds. In Hindi. From any phone. That just happened."

---

**[01:10 – 01:45 — THE PROBLEM (voiceover over text/graphics)]**
*[Cut to slides or simple text on screen]*

**HOST (voiceover):**
"Four hundred million Indians are entitled to PM-Kisan money. MGNREGA wages. Ayushman Bharat health coverage.

But to find out if they qualify — how to apply, whom to call — they have to navigate government websites, in English, on a smartphone they don't have.

ASHA workers are overworked. Helplines have 45-minute waits. And misinformation spreads faster than the truth.

JanAI is a phone number. That's it. Anyone who can dial can access thirty government schemes, live crop market prices, and health guidance — in their own language, in under four seconds."

---

**[01:45 – 02:20 — THE TECH (screen recording of Live Call on website)]**
*[Screen recording: open janai.vercel.app. Show the website briefly. Click "Try on Web". Make a browser call.]*

**HOST (voiceover):**
"Under the hood:

A caller speaks. Twilio transcribes the speech. AWS Lambda receives the query. Amazon Bedrock — our AI layer — runs it through a verified knowledge base using semantic search. Sarvam AI converts the answer to voice in the caller's language. Back to the caller in four seconds.

We also have three specialized AI agents — Arya for government schemes and legal rights, Hitesh for farming and mandi prices, Vidya for health and mental wellness. Each has its own voice, its own personality, and routes automatically based on what you ask."

*[Show voice selection on website, briefly.]*

---

**[02:20 – 02:50 — THE KNOWLEDGE LAYER]**
*[Back to host on camera OR continue screen recording]*

**HOST (to camera):**
"But fast AI is useless if the information is wrong.

JanAI has a verified knowledge base. Every piece of information — eligibility criteria, helpline numbers, application steps — is reviewed by both an AI fact-checker and a human approver before it enters the system.

Because one wrong helpline number to someone in a mental health crisis is not acceptable."

*[Brief pause. Let that land.]*

"We also pull live data where it matters most — mandi crop prices from thirty-one hundred markets in India, via data.gov.in, updated every day."

---

**[02:50 – 03:20 — IMPACT & CLOSE]**
*[Cut to final slide / brand card]*

**HOST (voiceover):**
"Five hundred million Indians. One phone number. Four seconds to an answer.

JanAI doesn't ask them to upgrade their phone.
Doesn't ask them to learn English.
Doesn't ask them to download anything.

It just picks up.

Team Kaizen. JanAI.  2026."

*[Show phone number LARGE on screen: +1 831 298 8145]*
*[Below number, show: "No international balance? janai.me → Call Me Back — we'll call you"]*

**HOST (to camera, directly):**
"Call it. Or visit janai.me and we'll call you. It'll answer."

*[Fade out.]*

---

## Video Production Notes
- Run time: ~3:30 — trim or expand the tech section if needed
- Add Hindi subtitles wherever the AI speaks Hindi — they're part of the demo, not an accessibility afterthought
- Don't use a voiceover for the live call section — the sound of a real phone ringing is worth more than any narration
- Background music: subtle instrumental, warm, slightly cinematic — not upbeat startup music, not sad. Think "documentary film score for something hopeful"
- Color grade: warm, slightly high contrast — not cold or clinical

---

---

# TASK 4 — THE HIGH-IMPACT SUMMARY
*(Use this as your written project summary / README excerpt / hackathon submission text)*

---

## JanAI — Voice AI for Every Indian

**The Wall Nobody Talks About**

India has 800 million mobile phone subscribers. But only 360 million have smartphones. The other 440 million — farmers, daily-wage workers, elderly people, first-generation literates — own phones that can call and text. That's it. Every AI assistant, every digital service, every government scheme update lives on the internet, in English, behind an app. For these 440 million people, the AI revolution might as well not exist.

This is the wall. It is built from three things: no smartphone, no reliable internet, and no English. JanAI knocks it down with one phone call.

**What JanAI Is**

JanAI is a voice-first AI assistant that anyone in India can reach by dialing a number — from the most basic ₹500 keypad phone. No app. No internet. No English required. The caller speaks naturally in Hindi, Marathi, Tamil, or English. Within four seconds, an AI responds in the same language with verified, accurate information — government scheme eligibility, live crop market prices, health guidance, legal rights.

It is not a menu system. It is not read-only scripted IVR. It is a full conversational AI that remembers the context of the conversation, routes to the right expert based on intent, pulls live data from government APIs, and handles emotional distress with sensitivity before referring to professional crisis helplines.

**The Technology**

The voice pipeline: Twilio handles telephony and speech recognition. AWS Lambda runs the serverless logic. Amazon Bedrock Nova Lite powers the language intelligence. Amazon Titan Embeddings enable semantic search across a verified knowledge base stored in DynamoDB. Sarvam AI's bulbul:v2 model converts text responses back to natural-sounding Indian-language voice. Total round-trip latency from speech to answer: 3.6 seconds.

Three distinct AI agent personalities handle different domains. Arya focuses on government schemes and legal rights. Hitesh covers agriculture, live mandi prices from 3,100 markets, and farming guidance. Vidya handles health, mental wellness, and emotional support. Routing between agents is automatic and seamless — callers just ask naturally.

**Why This Is Necessary**

India's PM-Kisan scheme has enrolled 120 million farmer families. Millions more are eligible but unenrolled because navigating the application process requires internet access or a trip to a CSC that may be 15 kilometres away. Ayushman Bharat covers 500 million people — but enrollment requires knowing you're eligible. Knowledge that is locked inside a website, behind a smartphone, in English, is knowledge that doesn't exist for the people who need it most.

JanAI's design principle is simple: every piece of critical information in the system is verified by both an AI review agent and a human approver before it reaches a caller. The system will never hallucinate a wrong helpline number to someone who just described being in crisis. Trust is not optional at this scale.

**The Proof**

The number +1 831 298 8145 is live. Call it. Ask in Hindi about PM-Kisan, or ask in Tamil about mandi prices for groundnuts in Karnataka, or ask in English about Ayushman Bharat eligibility criteria. It will answer in four seconds. This is a working, deployed product — not a mockup, not a prototype with caveats.

We built this in four days after being selected from the initial submission round of  2026. The initial submission took 90 minutes. The idea was simple enough to pitch in two sentences and complex enough to take four days of serious engineering to build correctly.

**The Ask**

JanAI is ready for a toll-free Indian number, a partnership with one state government, and the chance to serve the farmers, families, and workers who have been waiting for AI to finally pick up the phone.

---

*Team Kaizen |  | *
*GitHub: github.com/jatin-karma/JanAI | Live: +1 831 298 8145*

---

---

# APPENDIX — JUDGE TALKING POINTS
*(If someone demos or presents live, know these answers)*

**Q: Is the phone number real?**
A: Yes. +1 831 298 8145. Works 24/7. Call it during the presentation.

**Q: Why a US number?**
A: Trial phase on Twilio. An Indian toll-free number requires a business registration — we're provisioning it. The AI, knowledge base, and entire backend are on Indian-region-capable AWS infrastructure (us-east-1 with plans for ap-south-1 Mumbai).

**Q: What model are you using?**
A: Amazon Bedrock Nova Lite as primary — cost-effective, low latency, configurable. OpenAI GPT-4o-mini as a configured fallback.

**Q: Not everyone has international call balance — how can they try it?**
A: Visit **janai.me** and use the "Call Me Back" feature — enter your Indian number and our system calls you. Completely free on the user's end. The call originates from our Twilio number so there's no international charge to the user.

**Q: How did you get 4-second latency?**
A: We identified the bottleneck was 4 sequential Sarvam TTS calls at ~2s each. Fixed with: parallel TTS execution via ThreadPoolExecutor, Bedrock converse_stream() instead of converse(), in-memory audio caching for static phrases, and Polly `<Say>` for non-critical filler text. Full write-up in the repo memory notes.

**Q: How do you prevent hallucinations?**
A: Two-layer verification. Every knowledge base entry is reviewed by a Bedrock Claude fact-check agent (PASS/FLAG/FAIL + reason) AND approved by a human admin before going live. Critical helpline numbers are hardcoded in the system prompt, not generated by the LLM.

**Q: What about Bhashini?**
A: Designed into the architecture as a drop-in replacement for Sarvam AI. Bhashini covers all 22 scheduled languages via a single government API. Onboarding required organizational approval that wasn't available within the hackathon window. We use Sarvam AI for the current 4 languages, which are the 4 highest-coverage languages covering ~70% of rural India.

**Q: Can this scale?**
A: AWS Lambda scales to thousands of concurrent calls automatically. At 1 lakh calls/month, cost drops to ₹4/call. Architecture is stateless — each call is independent.
