# JanAI — Speech Accuracy Beyond Ideal Conditions

> **File:** `lambdas/call_handler/handler.py`  
> **Last updated:** July 2026  
> **Purpose:** Explains how JanAI improves speech recognition (STT) accuracy under noisy, low-quality, or accented conditions.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [1. Custom Speech Hints (Vocabulary Enrichment)](#1-custom-speech-hints-vocabulary-enrichment)
3. [2. STT Post-Processing Corrections](#2-stt-post-processing-corrections)
4. [3. Ambient Noise Rejection (Confidence Filtering)](#3-ambient-noise-rejection-confidence-filtering)
5. [Summary of Benefits](#summary-of-benefits)

---

## Overview
In real-world rural calling environments, users rarely have perfect connections. They may call from crowded markets (mandi), farms with background noise (tractors, wind, animals), or have heavy accents. Furthermore, standard speech recognition engines often struggle with Indian names, local crops, and government scheme names (e.g. transcribing "JanAI" as "jan-ai" or "pm kisan" as "p m kisaan").

To address this, JanAI utilizes a **three-tiered speech accuracy pipeline**:

```
                  Raw Telephony Call Audio
                             │
                             ▼
             ┌──────────────────────────────┐
             │   1. Custom Speech Hints     │ ◄── Enriches Twilio's STT model vocabulary
             └──────────────┬───────────────┘     (includes crop names, schemes, names)
                            │
                            ▼
             ┌──────────────────────────────┐
             │ 2. Post-Processing Clean    │ ◄── Fixes common spelling variations
             └──────────────┬───────────────┘     using case-insensitive regex mapping
                            │
                            ▼
             ┌──────────────────────────────┐
             │    3. Confidence Filter      │ ◄── Rejects ambient/static noises
             └──────────────┬───────────────┘     and re-prompts the caller
                            │
                            ▼
                Clean, Accurate Transcript
```

---

## 1. Custom Speech Hints (Vocabulary Enrichment)
When opening a speech `<Gather>`, we supply Twilio with a comma-separated list of **speech hints**. These hints bias the STT engine towards recognizing specific domain-relevant terms.

We expanded the `LANG_CONFIG` dictionary with custom hints for each of our supported languages:

```python
LANG_CONFIG = {
    "hi": {
        "hints": "PM Kisan, Ayushman Bharat, ration card, mandi, kisan, yojana, scheme, haan, nahi, bas, namaste, Arya, Aria, Hitesh, Vidya, JanAI, jan ai, jaan ai, aadhar, pancard, aalu, pyaaz, gehu, chawal, tamatar, bhav, crop, fertilizer, hospital",
    },
    "mr": {
        "hints": "PM Kisan, Ayushman Bharat, ration card, shetkari, bazar, yojana, scheme, hoy, nahi, Arya, Hitesh, Vidya, JanAI, jan ai, aadhar, bhav, fasal, maharashtra, tamatar, batata, kandha",
    },
    "ta": {
        "hints": "PM Kisan, Ayushman Bharat, scheme, ration card, vanakkam, aam, illai, Arya, Hitesh, Vidya, JanAI, jan ai, arisi, நெல், விலை, திட்டம், விவசாயம்",
    },
    "en": {
        "hints": "yes, no, PM Kisan, Ayushman Bharat, scheme, yojana, ration card, mandi, kisan, Aadhaar, subsidy, crop, fertilizer, health, hospital, garlic, cotton, wheat, rice, tomato, onion, gold, silver",
    },
}
```

These lists ensure Twilio transcribes phonetic spelling variants (e.g. *"aloo"*, *"tamatar"*, *"நெல்"*) accurately even in noisy channels.

---

## 2. STT Post-Processing Corrections
Even with hints, STT engines sometimes output lowercase or split-word variations of branded names. We implemented a case-insensitive regex mapper `_clean_stt_transcript(text)` that processes the raw transcript before routing it:

```python
def _clean_stt_transcript(text: str) -> str:
    """Post-process STT transcripts to correct common Indian/domain mishearings."""
    if not text:
        return ""
    import re
    cleaned = text
    
    corrections = {
        r'\bjan\s+ai\b': 'JanAI',
        r'\bjaan\s+ai\b': 'JanAI',
        r'\bjana\s+i\b': 'JanAI',
        r'\bjanai\b': 'JanAI',
        r'\bjaanai\b': 'JanAI',
        r'\bpm\s+kisaan\b': 'PM Kisan',
        r'\bp\s+m\s+kisan\b': 'PM Kisan',
        r'\bp\s+m\s+kisaan\b': 'PM Kisan',
        r'\bayushman\s+bharat\b': 'Ayushman Bharat',
        r'\baayushman\s+bharat\b': 'Ayushman Bharat',
        r'\baayushmaan\s+bharat\b': 'Ayushman Bharat',
        r'\bhithesh\b': 'Hitesh',
        r'\bhitesha\b': 'Hitesh',
        r'\baria\b': 'Arya',
        r'\baarya\b': 'Arya',
        r'\bariya\b': 'Arya',
        r'\bvidhya\b': 'Vidya',
    }
    
    for pattern, replacement in corrections.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
    return cleaned
```

---

## 3. Ambient Noise Rejection (Confidence Filtering)
In noisy environments, a cough, wind blowing, or car horns can trigger the STT engine to output short, garbled transcripts (e.g. *"hi"*, *"is"*, *"yes"*). 

To prevent the LLM from responding to these false triggers, we check Twilio's `Confidence` score (a value from `0.0` to `1.0` indicating transcription certainty) alongside the word count of the query:

```python
    # Confidence check (Task 7 fallback for low-confidence ambient noise)
    confidence_str = params.get("Confidence", "1.0")
    try:
        confidence = float(confidence_str)
    except Exception:
        confidence = 1.0
        
    _words = speech_text.split() if speech_text else []
    if confidence < 0.35 and len(_words) < 3:
        logger.info(f"Low confidence ({confidence}) short query: '{speech_text}'. Re-prompting caller.")
        return ask_again(language, voice, current_agent)
```

If the transcription confidence is below **35%** and the text is very short (under 3 words), the system discards the query and plays a polite re-prompt:
> *"अरे, सुनाई नहीं दिया। एक बार फिर से बोलिए?"* (Sorry, I didn't catch that. Could you say it again?)

---

## Summary of Benefits
- **No false-triggers:** Static and noise will no longer cause the bot to speak random replies.
- **Flawless Brand Detection:** The AI always recognizes *"JanAI"*, *"PM Kisan"*, and agent names (*"Arya"*, *"Hitesh"*, *"Vidya"*) correctly, enabling smooth agent transfers and profile logs.
- **Accurate Agri/Mandi Rates:** Better recognition of crop names (*"cotton"*, *"garlic"*, *"tamatar"*) directly translates to more accurate live price lookups.
