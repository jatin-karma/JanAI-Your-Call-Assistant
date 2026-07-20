# Implementation Plan - Address Call Quality, Speech Pace, and Call Responsiveness

This plan addresses several key issues causing poor response quality, fast speech, and call dropping in the JanAI voice call agent.

## User Review Required

We have identified the root causes for the AI not responding well on calls:
1. **Silence / Timeout Call Drops**: Currently, if the caller is silent for a few seconds, the Twilio `<Gather>` times out. In the fast path and poll success handlers, this falls through to a goodbye message and then hangs up. In greeting/welcome handlers, it hangs up immediately with no message. This leads to abrupt call drops if the caller takes a moment to think.
   - *Fix*: We will add a fallback `<Redirect>` inside `_append_listen_gather` right after the `<Gather>` verb. If the user is silent, it will redirect back to `/voice/gather`, which triggers `ask_again` ("Sorry, I didn't catch that. Could you say it again?") to keep the conversation alive.
2. **Incorrect Marathi Speech Recognition**: In `_append_listen_gather`, the STT language is overridden to `"hi-IN"` (Hindi) for Marathi callers. This forces Twilio to transcribe Marathi speech as Hindi, resulting in gibberish or empty transcripts that trigger error responses.
   - *Fix*: We will use the correct configured language (`cfg["twilio_speech_lang"]`) directly.
3. **Speech Pace Issue**: The `sarvam_tts` payload has a hardcoded `"pace": 1.25` parameter, making the agent speak 25% faster than normal. This is too fast for telephony calls and makes responses hard to follow, especially for rural audiences.
   - *Fix*: We will reduce the pace to a natural `1.0` value.
4. **Agent Identity Conflict**: In `lambdas/call_handler/handler.py`, the `build_system_prompt` function contains a bug where `Your name is Arya.` is hardcoded in the prompt base even when the active agent is `hitesh` or `vidya`. This conflicts with the agent personality descriptions and degrades output quality.
   - *Fix*: Make the prompt base dynamic using `Your name is {name_display}.`
5. **Web Agent Placeholder Issue**: In `lambdas/web_agent/handler.py`, the system prompt starts with `You are your name, the AI web assistant`, which contains a literal template/placeholder error.
   - *Fix*: Replace it with `You are Vaani, the AI web assistant`.

## Proposed Changes

### compute

#### [MODIFY] [handler.py](file:///d:/Downloads/JanAI/JanAI/lambdas/call_handler/handler.py)
- In `_append_listen_gather`:
  - Change `_stt_lang` logic to use `cfg["twilio_speech_lang"]` for Marathi (`mr`), allowing native `mr-IN` speech recognition.
  - Append a `<Redirect>` element pointing to `gather_url` so that if the user does not speak, the call redirects back to gather, prompting the user with `ask_again` instead of hanging up.
- In `sarvam_tts`:
  - Change `"pace": 1.25` to `"pace": 1.0` for natural speech.
- In `build_system_prompt`:
  - Replace `Your name is Arya.` with `Your name is {name_display}.` to align with the chosen agent's persona.

#### [MODIFY] [handler.py](file:///d:/Downloads/JanAI/JanAI/lambdas/web_agent/handler.py)
- In `VAANI_SYSTEM_PROMPT`:
  - Replace `You are your name, the AI web assistant` with `You are Vaani, the AI web assistant`.

## Verification Plan

### Automated Tests
- Perform python syntax checks on the modified files.

### Manual Verification
- Review prompt construction strings and Twilio TwiML responses to verify that:
  - Correct agent names are formatted in prompts.
  - TwiML outputs contain `<Redirect>` tags right after `<Gather>`.
  - Marathi calls utilize `<Gather language="mr-IN">`.
