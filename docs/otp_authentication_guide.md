# 🔐 JanAI Twilio Verify & Phone OTP Authentication Guide

This document provides a comprehensive technical overview of JanAI's **Phone Number SMS OTP Authentication System**, including how it bridges voice call history to web profiles, how the Twilio Verify API operates under the hood, and the exact manual steps required to set up Twilio credentials.

---

## 📐 Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │    TWILIO VERIFY & OTP SYSTEM FLOW     │
                      └────────────────────────────────────────┘
                                           │
        ┌──────────────────────────────────┴──────────────────────────────────┐
        │                                                                     │
        ▼                                                                     ▼
[1. Real SMS OTP Flow (Twilio Verify)]                      [2. Demo Bypass Mode ("123456")]
Sends real SMS code to +91 9876543210                       Entering code 123456 instantly approves
Requires: TWILIO_VERIFY_SERVICE_SID                         login without SMS delays or Twilio fees.
```

---

## 🔑 Manual Credentials Required from You

To enable live SMS OTP delivery via Twilio, you need to configure 3 environment variables in your AWS Lambda environment:

| Variable Name | Example Value | Where to Find in Twilio Console |
|---|---|---|
| **`TWILIO_ACCOUNT_SID`** | `YOUR_TWILIO_ACCOUNT_SID` | Twilio Console Dashboard Header |
| **`TWILIO_AUTH_TOKEN`** | `YOUR_TWILIO_AUTH_TOKEN` | Twilio Console Dashboard Header |
| **`TWILIO_VERIFY_SERVICE_SID`** | `YOUR_TWILIO_VERIFY_SERVICE_SID` | Twilio Console $\rightarrow$ Verify $\rightarrow$ Services |

### 🛠️ Step-by-Step Instructions to Create `TWILIO_VERIFY_SERVICE_SID`:

1. Log into your [Twilio Console](https://console.twilio.com/).
2. In the left navigation menu, go to **Explore Products $\rightarrow$ Verify $\rightarrow$ Services**.
3. Click **Create Service**.
4. Set **Friendly Name** to `JanAI-Auth`.
5. Set **Code Length** to `6 digits`.
6. Click **Create**.
7. Copy the generated **Service SID** (starts with `VA...`) and set it as `TWILIO_VERIFY_SERVICE_SID` in AWS Lambda.

---

## ⚙️ How the OTP System Operates (API Request / Response Flow)

### 1. Sending the OTP (`POST /auth/send-otp`)

#### **Request (Frontend $\rightarrow$ Lambda):**
```json
POST /auth/send-otp
Content-Type: application/json

{
  "phone": "+919876543210"
}
```

#### **Backend Execution (Lambda):**
```python
verification = twilio_client.verify.v2.services(TWILIO_VERIFY_SERVICE_SID) \
    .verifications.create(to="+919876543210", channel="sms")
```

#### **Response (Lambda $\rightarrow$ Frontend):**
```json
{
  "status": "success",
  "message": "OTP sent successfully to +919876543210"
}
```

---

### 2. Verifying the OTP (`POST /auth/verify-otp`)

#### **Request (Frontend $\rightarrow$ Lambda):**
```json
POST /auth/verify-otp
Content-Type: application/json

{
  "phone": "+919876543210",
  "code": "849201"
}
```

#### **Backend Verification Logic (Lambda):**
```python
# 1. Demo Bypass Check
if code == "123456":
    return approve_login(phone="+919876543210")

# 2. Live Twilio Verify API Check
verification_check = twilio_client.verify.v2.services(TWILIO_VERIFY_SERVICE_SID) \
    .verification_checks.create(to="+919876543210", code=code)

if verification_check.status == "approved":
    return approve_login(phone="+919876543210")
else:
    raise Exception("Invalid or expired OTP code")
```

#### **Response (Lambda $\rightarrow$ Frontend):**
```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "phone": "+919876543210",
    "name": "JanAI User"
  }
}
```

---

## 📱 How 1 OTP Completes BOTH Actions Simultaneously

A single 6-digit OTP code accomplishes **2 critical tasks at once**:

1. **Twilio Phone Verification:** Confirms the user owns the phone number, allowing outbound Twilio callback calls and SMS summaries.
2. **Website Login & Call History Sync:** Logs the user into the JanAI website profile (`/profile`) and automatically renders all past voice calls matching `+919876543210`.

---

## ⚡ Demo Bypass Mode (`123456`)

For hackathon demonstrations, client presentations, or offline testing without SMS carrier fees or network delays:
* Typing **`123456`** into the OTP field immediately verifies the phone number and logs in within 1 millisecond.
