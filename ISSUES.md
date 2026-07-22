# JanAI — Known Issues & Fix Guide
> Last Updated: 22 July 2026 | Audited by: Antigravity AI

---

## 🔴 HIGH PRIORITY ISSUES

---

### Issue #1 — RAG Does Full Table Scan on Every Call

**File:** `lambdas/call_handler/handler.py` · Line `3598`  
**Severity:** 🔴 High — Performance degrades linearly as knowledge base grows

#### Root Cause
The `retrieve_context()` function calls `vectors_table.scan()` with no limit, downloading **every single document** from DynamoDB on every RAG query. At 100+ documents this takes 3–6 seconds.

#### Current Code
```python
# Line 3598
items = vectors_table.scan().get("Items", [])
```

#### Fix
Add a `Limit` guard and use paginated scan with a hard cap:
```python
# Option A: Quick fix — cap at 200 items (enough for current KB size)
items = vectors_table.scan(Limit=200).get("Items", [])

# Option B: Proper fix — paginate with projection (avoids reading full text during scan)
paginator = vectors_table.meta.client.get_paginator("scan")
items = []
for page in paginator.paginate(
    TableName="janai-vectors",
    ProjectionExpression="embedding, text_hi, text_en, text_mr, text_ta, title",
    PaginationConfig={"MaxItems": 300}
):
    items.extend(page.get("Items", []))
```

> **Long-term fix:** Migrate to AWS OpenSearch Serverless or Pinecone for proper vector search with O(log n) lookup.

---

### Issue #2 — Returning Caller Personalized Greeting Only Works for Hindi

**File:** `lambdas/call_handler/handler.py` · Line `2218`  
**Severity:** 🔴 High — Tamil/Marathi users get English greeting on return call

#### Root Cause
The personalized greeting for returning callers only has a Hindi branch and falls back to English for all other languages.

#### Current Code
```python
# Line 2218
greeting = f"नमस्ते {stored_name} जी! जन-एआई में आपका स्वागत है। मैं आपकी क्या सहायता कर सकती हूँ?" \
    if stored_lang == "hi" \
    else f"Hello {stored_name}! Welcome to JanAI. How can I assist you today?"
```

#### Fix — Add all 4 language branches + agent gender awareness
```python
_gender = agent_cfg.get("gender", "female")
if stored_lang == "hi":
    _verb = "कर सकती हूँ" if _gender == "female" else "कर सकता हूँ"
    greeting = f"नमस्ते {stored_name} जी! जन-एआई में आपका स्वागत है। मैं आपकी क्या मदद {_verb}?"
elif stored_lang == "mr":
    _verb = "करू शकते" if _gender == "female" else "करू शकतो"
    greeting = f"नमस्कार {stored_name}! जन-एआई मध्ये पुन्हा स्वागत. मी तुमची कशी मदत {_verb}?"
elif stored_lang == "ta":
    greeting = f"வணக்கம் {stored_name}! JanAI-க்கு மீண்டும் வரவேற்கிறோம். உங்களுக்கு எப்படி உதவட்டும்?"
else:
    greeting = f"Hello {stored_name}! Welcome back to JanAI. How can I assist you today?"
```

---

### Issue #3 — WebRTC Browser Call Token Limit = 3 Per IP Per Day

**File:** `lambdas/call_handler/handler.py` · Line `703`  
**Severity:** 🔴 High — Judges/investors/demo visitors share office IP, hit limit after 3 calls

#### Root Cause
Production uses a hard-coded limit of 3 WebRTC tokens per IP per day. People demoing from the same WiFi (office, event, hackathon) share one NAT IP and all 3 slots are consumed quickly.

#### Current Code
```python
MAX_TOKENS_PER_DAY = 1000 if os.environ.get("APP_ENV") == "development" else 3
```

#### Fix
```python
# Read from environment so it can be tuned without redeploy
MAX_TOKENS_PER_DAY = int(os.environ.get("MAX_TOKENS_PER_DAY", "20"))
```

---

### Issue #4 — Agent Switch Always Triggers on Name Mention

**File:** `lambdas/call_handler/handler.py` · Line `2623`  
**Severity:** 🔴 High — Causes unintended mid-conversation agent switches

#### Root Cause
The boolean guard `(has_switch_phrase or True)` is **always `True`** regardless of `has_switch_phrase`. This means any mention of an agent name (e.g. "Arya, tell me about PM Kisan") incorrectly triggers an agent switch.

#### Current Code
```python
# Line 2623 — BUG: (has_switch_phrase or True) is ALWAYS True
explicitly_named = agent_named and (has_switch_phrase or True)  # name alone is enough
```

#### Fix — Recommended: allow name alone only if name starts the utterance
```python
# Switch if: name mentioned + (explicit switch phrase OR name appears at start of sentence)
text_trimmed = speech_text.lower().strip()
name_at_start = any(text_trimmed.startswith(t) for t in name_triggers.get(requested_agent, []))
explicitly_named = agent_named and (has_switch_phrase or name_at_start)
```

---

## 🟡 MEDIUM PRIORITY ISSUES

---

### Issue #5 — Login/Register Does Full DynamoDB Table Scan

**File:** `lambdas/call_handler/handler.py` · Lines `1594`, `1672`  
**Severity:** 🟡 Medium — Slow at scale (> 5,000 users)

#### Root Cause
Every login, register, and password reset scans the entire `janai_users` table filtered by email. DynamoDB scan is O(n) — it reads ALL items to find a match.

#### Current Code
```python
existing = users_table.scan(
    FilterExpression="email = :e",
    ExpressionAttributeValues={":e": email},
)
```

#### Fix
**Step 1:** Create a GSI (Global Secondary Index) on `email` in AWS Console:
```
DynamoDB → janai_users → Indexes → Create GSI
  Partition key: email (String)
  Index name: email-index
```

**Step 2:** Replace `scan()` with `query()`:
```python
existing = users_table.query(
    IndexName="email-index",
    KeyConditionExpression="email = :e",
    ExpressionAttributeValues={":e": email},
)
```

---

### Issue #6 — Admin Calls Page Scans Entire Calls Table with No Limit

**File:** `lambdas/call_handler/handler.py` · Line `1964`  
**Severity:** 🟡 Medium — Slow at high call volume (> 10,000 calls)

#### Fix
```python
# Add Limit to cap the scan
result = calls_table.scan(
    FilterExpression="from_number = :ph",
    ExpressionAttributeValues={":ph": phone},
    Limit=100  # Cap at 100 most recent records
)
```

---

### Issue #7 — Returning Hitesh Caller Gets Feminine Grammar in Greeting

**File:** `lambdas/call_handler/handler.py` · Line `2218`  
**Severity:** 🟡 Medium — Grammatically wrong for Hitesh (male agent)

#### Root Cause
The hardcoded greeting uses `कर सकती हूँ` (feminine) even when the caller's preferred agent is Hitesh (male).

**Fix:** Already covered by Issue #2 fix — the gender-aware branch selects the correct verb form per agent.

---

### Issue #8 — Language Defaults to `"en"` for Unknown Phone Callers

**File:** `lambdas/call_handler/handler.py` · Line `2159`  
**Severity:** 🟡 Medium — Analytics/call logs show wrong language for Indian phone callers

#### Current Code
```python
language = lang_param if (lang_param in LANG_CONFIG) else (
    caller_profile.get("language", "en") if caller_profile else "en"
)
```

#### Fix — Default to `"hi"` for unknown Indian phone callers
```python
language = lang_param if (lang_param in LANG_CONFIG) else (
    caller_profile.get("language", "hi") if caller_profile else "hi"
)
```

---

## 🟢 LOW PRIORITY ISSUES

---

### Issue #9 — Acknowledgement Messages Use Single TTS Call (Not Parallel)

**File:** `lambdas/call_handler/handler.py` · ~Line `2865`  
**Severity:** 🟢 Low — Minor latency improvement possible

#### Fix
Replace `sarvam_tts(ack_text, ...)` calls in the data-fetch path with `_tts_chunks_parallel(ack_text, ...)` to pre-generate ack audio in parallel with the data API call.

---

### Issue #10 — `.env` File with Secrets Should Not Be in Repository

**File:** `.env`  
**Severity:** 🟢 Low (security-sensitive if repo is public)

#### Fix
```bash
# 1. Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# 2. Remove from git tracking (keeps file locally, never deletes it)
git rm --cached .env
git rm --cached .env.local 2>/dev/null || true

# 3. Commit the removal
git commit -m "chore: remove .env from git tracking (keep secrets out of repo)"
```

**Secrets should live in:**
- **AWS Lambda:** Environment Variables tab in Lambda console ✅ (already done)
- **Local dev:** `.env` file locally (not committed)
- **CI/CD:** GitHub Secrets / AWS Parameter Store

---

## 📋 Fix Priority Matrix

| # | Issue | Severity | File | Line(s) | Effort | Status |
|:--|:---|:---|:---|:---|:---|:---|
| 1 | RAG full table scan | 🔴 High | handler.py | 3598 | Medium | 🔲 Open |
| 2 | Returning caller greeting (Marathi/Tamil) | 🔴 High | handler.py | 2218 | Easy | 🔲 Open |
| 3 | WebRTC token limit = 3/day | 🔴 High | handler.py | 703 | Easy | 🔲 Open |
| 4 | Agent switch always triggers | 🔴 High | handler.py | 2623 | Easy | 🔲 Open |
| 5 | Login scan — no email GSI | 🟡 Medium | handler.py | 1594, 1672 | Hard | 🔲 Open |
| 6 | Admin scan has no limit | 🟡 Medium | handler.py | 1964 | Easy | 🔲 Open |
| 7 | Hitesh greeting uses feminine grammar | 🟡 Medium | handler.py | 2218 | Easy | 🔲 (with #2) |
| 8 | Language defaults to "en" for phone | 🟡 Medium | handler.py | 2159 | Easy | 🔲 Open |
| 9 | Ack TTS not parallelized | 🟢 Low | handler.py | ~2865 | Medium | 🔲 Open |
| 10 | .env file in repository | 🟢 Low | .env | — | Easy | 🔲 Open |
