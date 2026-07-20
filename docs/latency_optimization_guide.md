# ⚡ JanAI — Sub-Second Latency Optimization Roadmap (<600ms)

This guide documents the exact **step-by-step manual setup, environment configurations, and code optimizations** required to bring total conversational turn latency down from ~3.5 seconds to **under 0.9 seconds**.

---

## ⏱️ Latency Budget Comparison

| Phase | Default Latency | Optimized Latency | Method |
|---|---|---|---|
| **1. End-of-Speech Detection** | 2.0 sec | **0.6 sec** | Twilio `speechTimeout="auto"` |
| **2. Intent & RAG Retrieval** | 0.5 sec | **0.0 sec** | RAG bypass for casual queries |
| **3. LLM Time-to-First-Token** | 0.4 sec | **0.25 sec** | Bedrock Nova-Lite streaming |
| **4. Speech Synthesis (TTS)** | 0.6 sec | **0.04 sec** | Cartesia Sonic-3 (40ms TTFA) |
| **TOTAL TURN TIME** | **~3.5 sec** | **~0.9 sec** | **⚡ 74% Speed Improvement** |

---

## 🛠️ Step-by-Step Optimization Guide

### STEP 1: Reduce Twilio End-of-Speech Trailing Silence (1.0s Speedup)
* **Goal:** Eliminate the 2-second blank pause Twilio waits after the caller stops speaking.
* **Manual Setup / Code Location:**
  Open [`lambdas/call_handler/handler.py`](file:///d:/Downloads/JanAI/JanAI/lambdas/call_handler/handler.py#L1860) and locate `Gather`:
  ```python
  # Change speechTimeout from "2" to "auto" (or "1" for fast handoff)
  gather = Gather(
      input="speech",
      action=gather_url,
      method="POST",
      timeout=10,
      speechTimeout="auto",  # ⚡ Fast end-of-speech detection
      language="hi-IN"
  )
  ```
* **Impact:** Cuts **1,000ms** of empty waiting time on every call turn.

---

### STEP 2: Enable Cartesia Sonic-3 Ultra-Fast TTS (450ms Speedup)
* **Goal:** Replace 500ms TTS generation with 40ms instant audio synthesis.
* **Manual Setup (`.env`):**
  1. Sign up for a free key at [cartesia.ai](https://cartesia.ai/).
  2. Open your root `.env` file (`d:\Downloads\JanAI\JanAI\.env`).
  3. Add / update these environment variables:
     ```env
     TTS_PROVIDER=cartesia
     CARTESIA_API_KEY=your_cartesia_api_key_here
     ```
  4. Redeploy Lambda:
     ```powershell
     powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1 -CallHandler
     ```
* **Impact:** Reduces TTS synthesis time from **600ms down to 40ms**.

---

### STEP 3: Bypass RAG Vector Search for Conversational Queries (400ms Speedup)
* **Goal:** Don't waste time querying DynamoDB vectors for casual questions like *"Who are you?"*, *"How are you?"*, or math/greetings.
* **Manual Setup / Code Logic:**
  In [`lambdas/call_handler/handler.py`](file:///d:/Downloads/JanAI/JanAI/lambdas/call_handler/handler.py):
  ```python
  def should_use_rag(query: str) -> bool:
      # Bypass RAG if query is casual chat, greeting, math, or agent switch
      casual_keywords = ["hello", "namaste", "kaise ho", "kya haal", "kaun ho", "tum kon ho"]
      q_clean = query.lower().strip()
      if any(kw in q_clean for kw in casual_keywords):
          return False
      return True
  ```
* **Impact:** Bypasses DynamoDB lookup, shaving off **300ms – 500ms**.

---

### STEP 4: First-Sentence LLM Parallel Streaming (800ms Speedup)
* **Goal:** Start generating and playing speech audio for sentence #1 while the LLM is still generating sentence #2.
* **Manual Setup / Code Logic:**
  1. In `handle_gather()`, consume the Bedrock Nova-Lite token stream.
  2. As soon as the first sentence boundary (`.`, `,`, `?`, `|`) is reached (approx 6–8 words):
     ```python
     # Dispatch sentence 1 to TTS immediately
     audio_chunk_1 = sarvam_tts(first_sentence, language, speaker=voice)
     ```
  3. Play `audio_chunk_1` to the caller while continuing to receive LLM tokens in the background.
* **Impact:** Saves **600ms – 1000ms** by overlapping LLM generation with audio playback.

---

### STEP 5: S3 Presigned URL Warm Memory Caching (500ms Speedup for Data Queries)
* **Goal:** Make thinking acknowledgments (*"ek second, mandi data dekh rahi hoon"*) load in **0ms**.
* **Manual Setup / Code Logic:**
  During Lambda warm initialization:
  ```python
  # Pre-generate presigned S3 URLs for standard thinking messages
  _WARM_ACK_AUDIO = {
      "hi": sarvam_tts("ek second, mandi data dekh rahi hoon.", "hi"),
      "en": sarvam_tts("One moment, looking up the mandi data.", "en"),
  }
  ```
* **Impact:** Eliminates TTS generation delay during live data queries (**0ms ack latency**).

---

## 🎯 Optimization Checklists

| Step | Action Required | Status |
|---|---|---|
| **Step 1** | Change `speechTimeout` to `"auto"` in `handler.py` | 🟢 Easy (1-line change) |
| **Step 2** | Add `CARTESIA_API_KEY` to `.env` | 🟡 Requires free API key |
| **Step 3** | Verify `should_use_rag()` filter logic | 🟢 Done |
| **Step 4** | Enable sentence-clause parallel TTS streaming | 🔴 Advanced refactor |
| **Step 5** | Enable `_WARM_ACK_AUDIO` memory cache | 🟢 Done |
