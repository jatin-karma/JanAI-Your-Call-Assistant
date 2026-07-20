# JanAI — Telephony Interruption Handling (Barge-in)

> **File:** `lambdas/call_handler/handler.py`  
> **Last updated:** July 2026  
> **Purpose:** Explains how JanAI handles interruptions (barge-in) during phone calls.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [What is Telephony Barge-in?](#what-is-telephony-barge-in)
3. [The Problem with the Old Flow](#the-problem-with-the-old-flow)
4. [The Solution: Nested TwiML Architecture](#the-solution-nested-twiml-architecture)
5. [TwiML Structure Comparison](#twiml-structure-comparison)
6. [Implementation Details](#implementation-details)
7. [Benefits of this Approach](#benefits-of-this-approach)

---

## Overview
In natural human conversation, people often interrupt the speaker to ask a clarification, change the topic, or say "stop". For a voice AI assistant, being able to handle interruptions (called **Barge-in**) is critical to feeling natural. 

Without barge-in, users feel like they are talking to a robotic IVR system where they must wait for the machine to finish speaking before they can reply.

---

## What is Telephony Barge-in?
Barge-in is a telephony media server feature. During a call, while the server is playing an audio file to the caller:
1. The server constantly listens to the incoming audio channel (the caller's microphone).
2. If it detects voice activity (energy/speech) above a certain threshold, the server **immediately stops playing the current audio**.
3. The server then captures the caller's speech and sends the transcript to the webhook URL.

---

## The Problem with the Old Flow
In the old implementation of `handler.py`, the audio playback and listening phases were separate and sequential:

```
┌─────────────────────────────────┐      ┌───────────────────────────────┐
│     Play Response Audio         │ ───► │  Append Gather (Listen)       │
│  (User CANNOT interrupt here)   │      │  (User can speak here)        │
└─────────────────────────────────┘      └───────────────────────────────┘
```

The TwiML generated was:
```xml
<Response>
    <!-- Playing response -->
    <Play>https://s3.amazonaws.com/.../audio1.wav</Play>
    <Play>https://s3.amazonaws.com/.../audio2.wav</Play>
    
    <!-- Listening (Starts ONLY after Play tags finish) -->
    <Gather input="speech" action="/voice/gather" method="POST" language="hi-IN" timeout="10" />
</Response>
```

If the response was 20 seconds long, the user was forced to listen to the whole 20 seconds. If they spoke during the `<Play>` phase, Twilio simply ignored their audio.

---

## The Solution: Nested TwiML Architecture
We solved this by nesting the `<Play>` and `<Say>` tags **inside** the `<Gather>` tag. 

In Twilio TwiML, when audio tags are nested inside `<Gather>`, Twilio keeps the speech recognition engine active *during* playback. Any speech detected from the user instantly interrupts the playback and posts the result to the `action` URL.

```
┌────────────────────────────────────────────────────────┐
│                      GATHER ACTIVE                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │               Play Response Audio                │ ─┼─► Speech Detected
│  │   (Playback immediately stops on interruption)   │  │   (Interrupts playback)
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## TwiML Structure Comparison

### Old Code (No Interruption)
```xml
<Response>
  <Play>https://s3.amazonaws.com/janai-tts/chunk1.wav</Play>
  <Gather input="speech" action="/voice/gather?lang=hi" language="hi-IN" timeout="10" />
</Response>
```

### New Code (With Barge-in Interruption)
```xml
<Response>
  <Gather input="speech" action="/voice/gather?lang=hi" language="hi-IN" timeout="10" enhanced="true">
    <Pause length="0.3" /> <!-- Telephony stabilization buffer -->
    <Play>https://s3.amazonaws.com/janai-tts/chunk1.wav</Play>
  </Gather>
</Response>
```

---

## Implementation Details

### 1. Updated Helper: `_append_listen_gather`
The helper function was modified to accept optional `audio_urls` and `text_to_say`, and nest them inside the `<Gather>` tag:

```python
def _append_listen_gather(response, language: str, voice: str = "", agent: str = "",
                          audio_urls: list = None, text_to_say: str = ""):
    ...
    g = Gather(
        input="speech",
        action=gather_url,
        method="POST",
        language=_stt_lang,
        speech_timeout="2", # triggers fast when user stops speaking
        timeout=10,
        hints=_all_hints,
        enhanced=True,
    )
    
    # Nest Play/Say inside Gather for natural Barge-in (interruption handling)
    if audio_urls:
        try: g.pause(length=0.3)
        except Exception: pass
        for url in audio_urls:
            g.play(url)
    elif text_to_say:
        try: g.pause(length=0.3)
        except Exception: pass
        g.say(text_to_say, voice=cfg["polly_voice"])
        
    response.append(g)
    response.redirect(gather_url)
```

### 2. Fast Path Integration (`handle_gather`)
For queries that skip the RAG database (e.g. greetings, simple conversation), we pass the pre-synthesis URLs to the gather:

```python
        if audio_urls:
            _append_listen_gather(response, language, voice, current_agent, audio_urls=audio_urls)
        else:
            _append_listen_gather(response, language, voice, current_agent, text_to_say=clean_answer)
```

### 3. RAG/Polling Path Integration (`handle_poll`)
For complex queries that require knowledge base or web search, once the background task finishes processing, we play the result with barge-in:

```python
    if answer:
        if audio_urls:
            _append_listen_gather(response, language, stored_voice, current_agent, audio_urls=audio_urls)
        else:
            audio_urls = _tts_chunks_parallel(answer, language, stored_voice)
            if audio_urls:
                _append_listen_gather(response, language, stored_voice, current_agent, audio_urls=audio_urls)
            else:
                _append_listen_gather(response, language, stored_voice, current_agent, text_to_say=answer)
```

---

## Benefits of this Approach

1. **Natural Interaction:** Users can cut off the bot mid-sentence if they hear their answer or if the bot misunderstood them.
2. **Cost-Efficient:** Stopping playback instantly saves Twilio telecom minutes (costs are calculated per second of audio played).
3. **No Latency Impact:** The interruption detection is handled completely by Twilio's media servers, adding **0ms** of latency to our backend.
4. **Telecom Line Stabilization:** The embedded `g.pause(length=0.3)` ensures the phone line audio path is fully established before audio plays, preventing the first syllable of the bot's response from getting cut off.
