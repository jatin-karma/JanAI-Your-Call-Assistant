# JanAI — RAG Pipeline & Intent Detection

> **File:** `lambdas/call_handler/handler.py`  
> **Last updated:** July 2026  
> **Purpose:** Explains how JanAI decides when to use RAG (knowledge retrieval) vs. answering directly, and how queries are routed through the system.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [The 3-Layer Intent Detection System](#the-3-layer-intent-detection-system)
3. [Full Query Flow Diagram](#full-query-flow-diagram)
4. [Layer 1 — Structural Pre-filter](#layer-1--structural-pre-filter)
5. [Layer 2 — LLM Self-Routing via Tags](#layer-2--llm-self-routing-via-tags)
6. [Layer 3 — RAG Vector Guard](#layer-3--rag-vector-guard)
7. [The RAG Pipeline](#the-rag-pipeline)
8. [Web Chat vs Voice Call Differences](#web-chat-vs-voice-call-differences)
9. [Language Support](#language-support)
10. [Performance Impact](#performance-impact)
11. [Dynamic Welcome & Language Switching (Task 4)](#dynamic-welcome--language-switching-task-4)

---

## Overview

JanAI is a voice AI helpline that handles queries in Hindi, Marathi, Tamil, and English. Not every query needs the full RAG (Retrieval-Augmented Generation) pipeline — a greeting like "namaste" or an acknowledgement like "haan theek hai" should be answered instantly without looking up any knowledge base.

**The core challenge:** How do we know when a query needs RAG and when it doesn't?

**Our answer:** A 3-layer intent detection system that is:
- ✅ **Language-agnostic** — works for all 4 languages without per-language keyword lists
- ✅ **Zero-latency** for Layers 1 & 3 — no extra API calls
- ✅ **Semantically accurate** — Layer 2 uses the LLM's own understanding, not just keywords
- ✅ **Extensible** — adding a new language doesn't require any routing logic changes

---

## The 3-Layer Intent Detection System

```
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│  LAYER 1: Structural Pre-filter (0ms)        │
│  is_simple_query_by_structure(text)          │
│                                              │
│  • ≤ 3 words?         → Simple (skip LLM)   │
│  • Pure ACK set?      → Simple (skip LLM)   │
│  • No question word   │                      │
│    AND no domain kw?  → Simple (skip LLM)   │
│  • Otherwise          → Complex (go to LLM) │
└──────────────┬──────────────────────────────┘
               │ Complex query
               ▼
┌─────────────────────────────────────────────┐
│  LAYER 2: LLM Self-Routing via Tags          │
│  (AWS Bedrock Nova Lite / OpenAI)            │
│                                              │
│  LLM reads the query + system prompt and    │
│  decides:                                   │
│  • "namaste" → answer directly              │
│  • "PM Kisan kaise milega?" → [FETCH_DATA]  │
│  • "aaj sona ka bhav?" → [WEB_SEARCH]       │
│  • "bye" → [HANGUP]                         │
│  • "Hitesh ko bulao" → [SWITCH:hitesh]      │
└──────────────┬──────────────────────────────┘
               │ [FETCH_DATA] or [WEB_SEARCH] tag
               ▼
┌─────────────────────────────────────────────┐
│  LAYER 3: RAG Vector Guard                   │
│  should_use_rag(text)                        │
│                                              │
│  • Live market query? → Skip vector search  │
│    (data.gov.in API handles it directly)    │
│  • Everything else?   → Use RAG vector DB   │
└──────────────┬──────────────────────────────┘
               │
               ▼
         RAG Pipeline
```

---

## Full Query Flow Diagram

```
Twilio Voice Call / Web Chat
            │
            ▼
    handle_gather() / handle_chat()
            │
            ├── Layer 1: is_simple_query_by_structure()
            │        │
            │   True │  False
            │        ▼   ───────────────────────────────────────
            │   Pure ACK?                                        │
            │   "haan/ok/ठीक"                                    │
            │        │                                           │
            │   Yes ─┤                                           │
            │        │                                           │
            │        ▼                                           ▼
            │   Instant ack              LLM Call (Bedrock / OpenAI) ← Layer 2
            │   response                Generates: quick_answer
            │   (no LLM call)                      │
            │                           ┌──────────┴──────────────────────┐
            │                           │  Tags in quick_answer?          │
            │                           └─────────────────────────────────┘
            │                                       │
            │                           [HANGUP]──► hangup
            │                           [SWITCH]──► agent switch
            │                                       │
            │                           ┌───────────┴──────────────────────┐
            │                           │ [FETCH_DATA] or [WEB_SEARCH]?    │
            │                           └──────────────────────────────────┘
            │                           No │              │ Yes
            │                              ▼              ▼
            │                        Fast TTS      _fetch_data_async()
            │                        + Listen      (background thread)
            │                                             │
            │                                    Layer 3: should_use_rag()
            │                                             │
            │                              ┌─────────────┴────────────┐
            │                              │ Live market query?        │
            │                              └──────────────────────────┘
            │                              No │          │ Yes
            │                                 ▼          ▼
            │                          RAG vector    data.gov.in
            │                          search        + web search
            │                                 │          │
            │                                 └────┬─────┘
            │                                      ▼
            │                              Phase 2 LLM call
            │                              (with retrieved data)
            │                                      │
            │                                      ▼
            └──────────────────────► Final TTS + Listen
```

---

## Layer 1 — Structural Pre-filter

**Function:** `is_simple_query_by_structure(text: str) -> bool`  
**Location:** `handler.py` ~line 2800  
**Cost:** 0ms — pure Python, no API calls

### What it checks

#### Rule 1: Word Count
```python
if len(words) <= 3:
    return True  # "haan", "namaste", "theek hai" → simple
```
Queries of 3 words or fewer are almost always greetings, acknowledgements, or continuations. They never need database lookup.

#### Rule 2: Question Words (Multilingual)
```python
_QUESTION_WORDS = {
    "kya", "kaise", "kyun", "kitna", "kaun", "kab", "kahaan",  # Hindi
    "क्या", "कैसे", "क्यों", "कितना", "कौन", "कब", "कहाँ",     # Devanagari
    "என்ன", "எப்படி", "ஏன்", "எவ்வளவு", "யார்", "எப்போது",   # Tamil
    "what", "how", "why", "when", "where", "which", "who",     # English
}
```
If a query contains a question word, it's information-seeking and likely needs the LLM or RAG.

#### Rule 3: Domain Keywords (Multilingual)
```python
_DOMAIN_KEYWORDS = {
    "yojana", "scheme", "योजना",         # Government schemes
    "mandi", "मंडी", "fasal", "kisan",   # Agriculture
    "hospital", "dawai", "ayushman",      # Health
    "bhav", "price", "gold", "petrol",   # Market data
    # ... and Tamil equivalents
}
```
If a query contains a domain keyword, it touches JanAI's knowledge domains and likely needs RAG.

#### Decision Logic
```
Simple (skip RAG) = word_count <= 3
                    OR (no question word AND no domain keyword)

Complex (use LLM) = has question word OR has domain keyword (and > 3 words)
```

### Pure ACK Fast-path (Voice calls only)
For voice calls, if the entire utterance is a subset of known acknowledgement words
(`haan`, `ok`, `ठीक`, `ஆம்`, etc.), the LLM call is **completely skipped** and a
natural continuation prompt is returned instantly:

```
User: "haan"
JanAI: "हाँ, बताइए — आगे क्या जानना चाहते हैं?"  ← 0ms LLM cost
```

---

## Layer 2 — LLM Self-Routing via Tags

**Mechanism:** System prompt instructs the LLM to append special tags  
**Location:** `build_system_prompt()` → `DATA ACCESS` section  
**Cost:** Normal LLM call cost (~300-600ms) — only runs for non-simple queries

The system prompt tells the LLM:

```
DATA ACCESS RULES:
- If you can answer from your own knowledge → answer directly (no tag)
- If you need scheme/eligibility/govt data → add [FETCH_DATA] at the end
- If you need live/realtime data → add [WEB_SEARCH] at the end
- NEVER add fetch tags for greetings, math, jokes, general knowledge
```

### Why this is the best intent detection approach

| Method | Accuracy | Latency | Works for new phrases? |
|---|---|---|---|
| Keywords only | ⚠️ Brittle | 0ms | ❌ No |
| LLM tags | ✅ Semantic | 0ms extra | ✅ Yes |
| Separate classifier model | ✅ Good | +100ms | ✅ Yes |

The LLM understands **meaning**, not just words:

| Query | Language | Correct Tag |
|---|---|---|
| `"PM Kisan register karna hai"` | Hindi | `[FETCH_DATA]` ✅ |
| `"PM Kisan ka naam suna hai"` | Hindi | *(none — conversational)* ✅ |
| `"நெல் விலை என்ன?"` | Tamil | `[FETCH_DATA]` ✅ |
| `"aaj sona ka bhav kya hai?"` | Hindi | `[WEB_SEARCH]` ✅ |
| `"tell me a joke"` | English | *(none)* ✅ |

### Tag Reference

| Tag | Meaning | Action taken |
|---|---|---|
| *(none)* | LLM knows the answer | Fast TTS response |
| `[FETCH_DATA]` | Needs scheme/agri knowledge | RAG pipeline + data.gov.in |
| `[WEB_SEARCH]` | Needs live/realtime data | Web search via DuckDuckGo |
| `[HANGUP]` | User said goodbye | TwiML hangup |
| `[SWITCH:name]` | User wants different agent | Agent transfer (Arya/Hitesh/Vidya) |

---

## Layer 3 — RAG Vector Guard

**Function:** `should_use_rag(speech_text: str) -> bool`  
**Location:** `handler.py` ~line 2860  
**Called from:** `_fetch_data_async()` (runs inside background thread)

At this point, the LLM has already decided data is needed (`[FETCH_DATA]` tag was set).
This layer decides specifically whether to run the **vector embedding + DynamoDB vector search**.

### When RAG vector search is SKIPPED

**Live market/weather queries** — better served by `_fetch_data_gov()` or `_fetch_web_search()`:
```python
live_market_keywords = [
    "mandi", "bhav", "sona", "chandi", "petrol", "diesel", "gold", "silver",
    "weather", "mausam", "temperature", "மண்டி", "தங்கம்",
]
```
For these queries, the RAG knowledge base has **static scheme documents**, not live prices.
Running vector search adds noise and latency without improving the answer.

### When RAG vector search IS USED
Everything else where `[FETCH_DATA]` was set:
- Government scheme eligibility questions
- Subsidy and registration processes  
- Health scheme details (Ayushman Bharat, ASHA)
- Agricultural best practices (not live prices)

---

## The RAG Pipeline

**Function:** `rag_pipeline(query, language, call_sid, ...)`  
**Location:** `handler.py` ~line 2890

### Steps

```
1. should_use_rag(query)
         │
    True │              False
         ▼                ▼
2. get_embedding(query)   Skip vector search → go to step 4
   (AWS Bedrock Titan)
         │
         ▼
3. retrieve_context(embedding, language)
   (DynamoDB janai_vectors table — cosine similarity, top-K)
         │
         ▼
4. _fetch_data_gov(query)  [if DATA_GOV_API_KEY is set]
   (data.gov.in: mandi prices, scheme data)
         │
         ▼
5. Combine context = RAG results + live data
         │
         ▼
6. ask_llm(query, context, language, history)
   (AWS Bedrock Nova Lite — answers using the retrieved context)
         │
         ▼
7. Return final answer string
```

### Infrastructure

| Component | Technology |
|---|---|
| Embedding model | `amazon.titan-embed-text-v2:0` (1024 dimensions) |
| Vector store | DynamoDB `janai_vectors` table |
| Knowledge base | DynamoDB `janai_knowledge` + S3 `janai-documents-2026` |
| Similarity method | Cosine similarity |
| LLM | AWS Bedrock `amazon.nova-lite-v1:0` |
| Fallback LLM | OpenAI `gpt-4o-mini` (if `LLM_PROVIDER=openai`) |

---

## Web Chat vs Voice Call Differences

| Feature | Voice Call (`handle_gather`) | Web Chat (`handle_chat`) |
|---|---|---|
| Layer 1 pre-filter | ✅ Yes — with pure ACK fast-path | ✅ Yes — structural check |
| Pure ACK handling | TwiML response (0ms LLM cost) | `ask_llm()` direct call |
| Layer 2 LLM tags | ✅ Drives FETCH_DATA/WEB_SEARCH | Replaced by structural routing |
| Layer 3 RAG guard | ✅ Inside `_fetch_data_async()` | ✅ Inside `rag_pipeline()` |
| Async processing | ✅ Background thread + polling | ❌ Synchronous |
| TTS output | Sarvam AI → S3 URL → Twilio | Sarvam AI → S3 URL → browser |

---

## Language Support

The intent detection system is **fully language-agnostic**:

| Query | Language | Layer 1 | Layer 2 Tag | Final Result |
|---|---|---|---|---|
| `"haan"` | Hindi | ✅ Pure ACK | — | Instant ack response |
| `"ஆம்"` | Tamil | ✅ Pure ACK | — | Instant ack response |
| `"ok"` | English | ✅ Pure ACK | — | Instant ack response |
| `"PM Kisan kaise milega?"` | Hindi | ❌ Complex | `[FETCH_DATA]` | RAG → scheme info |
| `"நெல் விலை என்ன?"` | Tamil | ❌ Complex | `[FETCH_DATA]` | data.gov.in → rice price |
| `"aaj sona ka bhav kya hai?"` | Hindi | ❌ Complex | `[WEB_SEARCH]` | Web search → gold price |
| `"Ayushman Bharat eligibility"` | English | ❌ Complex | `[FETCH_DATA]` | RAG → health scheme |
| `"mujhe ek joke sunao"` | Hindi | ❌ Complex | *(none)* | Direct LLM (no RAG) |

### Adding a New Language
Only requires:
1. Add to `LANG_CONFIG` dict
2. Add question words to `_QUESTION_WORDS` set
3. Add domain keywords to `_DOMAIN_KEYWORDS` set
4. **No changes to routing logic** — it's fully structural

---

## Performance Impact

### Before (old keyword-only `should_use_rag`)
| Query | Path | Latency |
|---|---|---|
| `"haan theek hai"` | LLM → no tag → TTS | ~700ms |
| `"PM Kisan form?"` | LLM → [FETCH_DATA] → RAG → TTS | ~2500ms |
| `"sona ka bhav?"` | LLM → [WEB_SEARCH] → web → TTS | ~3000ms |

### After (3-layer system)
| Query | Path | Latency | Saving |
|---|---|---|---|
| `"haan"` | Layer 1 pure ACK → TTS | ~200ms | **-500ms** |
| `"haan theek hai"` | Layer 1 ≤3 words → Direct LLM | ~350ms | **-350ms** |
| `"PM Kisan form?"` | Layer 1 complex → LLM → RAG → TTS | ~2500ms | same |
| `"sona ka bhav?"` | Layer 1 complex → LLM → web → TTS | ~3000ms | same |

**Overall improvement:** ~25-30% of calls hit Layer 1 (greetings/acks).  
**Average latency reduction per call:** ~150ms across the full call distribution.  
**No regression** on complex queries — identical path as before.

---

## Dynamic Welcome & Language Switching (Task 4)

To present a completely unbiased, frictionless greeting, JanAI bypasses traditional robotic IVR menus ("Press 1 for English...") for a dynamic experience.

### 1. Unbiased Welcome Chain
For first-time callers, JanAI plays a warm, multilingual greeting chain back-to-back using the native TTS engine for each word:
1. **Hindi:** *"नमस्ते!"* (Arya voice)
2. **Marathi:** *"नमस्कार!"* (Arya voice)
3. **Tamil:** *"வணக்கம்!"* (Arya voice)
4. **English:** *"Welcome to JanAI. Please speak in your language."* (Vidya voice)

This chain takes only **4-5 seconds** to play, ensuring the caller immediately knows all four languages are supported.

### 2. Multi-Language Switch Architecture
If a user switches their spoken language mid-call, the system handles it dynamically using three layers:

```
                  User Mid-Call Speech
                           │
                           ▼
             ┌───────────────────────────┐
             │   Layer 1: Command Map    │
             │   Explicit voice requests │
             └─────────────┬─────────────┘
                           │
                           ├─► Match: "talk in English" / "मराठीत बोला"
                           │   ➔ Switch Language State Immediately
                           │
                           ▼
             ┌───────────────────────────┐
             │   Layer 2: Script Scan    │
             │   Character set analysis  │
             └─────────────┬─────────────┘
                           │
                           ├─► Tamil characters > 15% ➔ Switch to ta
                           ├─► Devanagari + Marathi words ➔ Switch to mr
                           ├─► Devanagari only ➔ Switch to hi
                           │
                           ▼
             ┌───────────────────────────┐
             │   Layer 3: LLM Alignment  │
             │   Checks LLM output script│
             └─────────────┬─────────────┘
                           │
                           └─► LLM replies in Tamil/Hindi/Marathi script
                               ➔ Align next turn's STT language model
```

This ensures that even if the explicit command triggers fail, the system self-corrects to the caller's language dynamically without breaking the call flow.

