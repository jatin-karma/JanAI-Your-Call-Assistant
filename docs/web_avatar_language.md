# JanAI — Multilingual Web Avatar (Vaani) Integration

> **Files:**  
> • `lambdas/web_agent/handler.py` (Web Avatar backend)  
> • `website/src/components/JanAIAgent/JanAIWidget.jsx` (Web Chat UI)  
> • `scripts/local_server.py` (Local proxy backend)  
> **Last updated:** July 2026  
> **Purpose:** Detailed walkthrough of the web widget dynamic language features.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [1. Local Server Route Mapping](#1-local-server-route-mapping)
3. [2. Backend Language Auto-Detection](#2-backend-language-auto-detection)
4. [3. Browser Language Greeting Autopilot](#3-browser-language-greeting-autopilot)
5. [4. Bi-directional Language Synchronization](#4-bi-directional-language-synchronization)

---

## Overview
In the initial codebase, the web chat widget (the Vaani avatar chatbot) was hardcoded to run in Hindi (`hi-IN`). Any English, Marathi, or Tamil input typed or spoken by users was processed as Hindi, resulting in broken transcripts and unnatural responses. Furthermore, the local Flask server didn't route web avatar endpoints, forcing developers to test on live AWS.

We have implemented a **fully dynamic, automated multilingual system** for the web avatar.

---

## 1. Local Server Route Mapping
We updated `scripts/local_server.py` to mount the `web_agent` Lambda handler side-by-side with the Twilio calling handler under `/janai/chat` and `/janai/stt`. 

To prevent naming collisions (since both folders contain a module named `handler`), we isolate namespaces dynamically:

```python
# Add Lambda handler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambdas", "call_handler"))
import handler as call_handler_mod
lambda_handler = call_handler_mod.lambda_handler
sys.path.pop(0)

# Add Web Agent handler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambdas", "web_agent"))
import handler as web_agent_mod
web_agent_handler = web_agent_mod.lambda_handler
sys.path.pop(0)
```

Now you can test both telephony calls and the web chat widget on the same local Flask server (`http://localhost:8000`).

---

## 2. Backend Language Auto-Detection
Instead of using basic client-side regex matching (which fails for romanized Hinglish/Marathi), we migrated the character-based language detection engine to `lambdas/web_agent/handler.py`:

```python
def handle_chat(event: dict) -> dict:
    ...
    # Auto-detect language dynamically from user query
    language = detect_language_from_speech(message) or input_lang
```

This dynamically detects Devanagari Hindi vs. Marathi (using function word ratios), Tamil characters, and romanized script variations.

---

## 3. Browser Language Greeting Autopilot
When the user opens the JanAI homepage, the avatar reads their browser locale (`navigator.language`) and automatically serves the greeting in their matching native language:

```javascript
const VAANI_GREETINGS = {
  hi: 'नमस्ते! 🙏 मैं JanAI हूँ — JanAI की web assistant...',
  en: 'Hello! 🙏 I am JanAI — your web assistant. You can ask me...',
  mr: 'नमस्कार! 🙏 मी JanAI आहे — JanAI ची वेब असिस्टंट...',
  ta: 'வணக்கம்! 🙏 நான் JanAI — JanAI இன் இணைய உதவியாளர்...'
}
```

If a visitor from Chennai opens the site, they are immediately greeted in Tamil. If a user from Mumbai opens the site, they are greeted in Marathi.

---

## 4. Bi-directional Language Synchronization
When the backend auto-corrects the language of the conversation, it returns the updated language in the JSON payload. The React component (`JanAIWidget.jsx`) instantly syncs its local state:

```javascript
const data = await res.json()
const finalLang = data.language || activeLang
setActiveLang(finalLang) // Update React State
```

Once `activeLang` is updated, the widget dynamically binds the browser's speech recognition and audio recorder locales:

```javascript
useEffect(() => {
  if (recognitionRef.current) {
    const langCodes = {
      hi: 'hi-IN', mr: 'mr-IN', ta: 'ta-IN', te: 'te-IN', kn: 'kn-IN', bn: 'bn-IN', en: 'en-IN'
    }
    recognitionRef.current.lang = langCodes[activeLang] || 'hi-IN'
  }
}, [activeLang])
```

This ensures that subsequent microphone recordings listen and transcribe in the correct language!
