import os
import json
import logging
import requests
import boto3
from urllib.parse import quote

logger = logging.getLogger("janai")
s3_client = boto3.client("s3")
S3_BUCKET = os.environ.get("S3_BUCKET", "janai-documents-2026")

class VoiceSynthesizer:
    """
    Production Object-Oriented Voice Synthesis Service.
    Handles Cartesia Sonic-3 (40ms TTFA) and Sarvam Bulbul TTS fallback.
    """

    SARVAM_VOICE_MAP = {
        "arya": {
            "hi": ("sarvam:v2", "arya"),
            "en": ("cartesia", "vidya"),
            "mr": ("sarvam:v2", "arya"),
            "ta": ("sarvam:v2", "arya"),
        },
        "hitesh": {
            "hi": ("sarvam:v2", "hitesh"),
            "en": ("sarvam:v2", "hitesh"),
            "mr": ("sarvam:v2", "hitesh"),
            "ta": ("sarvam:v2", "hitesh"),
        },
        "vidya": {
            "hi": ("sarvam:v2", "vidya"),
            "en": ("cartesia", "vidya"),
            "mr": ("sarvam:v2", "vidya"),
            "ta": ("sarvam:v2", "vidya"),
        },
    }

    CARTESIA_VOICE_IDS = {
        "vidya": "846d67e0-c730-49d5-8820-d7039207038d",  # Sonic-3 English/Hinglish
        "arya":  "846d67e0-c730-49d5-8820-d7039207038d",
        "hitesh":"846d67e0-c730-49d5-8820-d7039207038d"
    }

    @classmethod
    def resolve_provider_and_speaker(cls, voice_name: str, language: str) -> tuple:
        voice = voice_name.lower()
        lang = language.lower()
        if voice in cls.SARVAM_VOICE_MAP and lang in cls.SARVAM_VOICE_MAP[voice]:
            return cls.SARVAM_VOICE_MAP[voice][lang]
        return ("sarvam:v2", "arya")

    @classmethod
    def synthesize_cartesia(cls, text: str, voice_name: str) -> bytes:
        api_key = os.environ.get("CARTESIA_API_KEY", "")
        if not api_key:
            raise ValueError("CARTESIA_API_KEY not configured")
        
        voice_id = cls.CARTESIA_VOICE_IDS.get(voice_name.lower(), cls.CARTESIA_VOICE_IDS["vidya"])
        url = "https://api.cartesia.ai/tts/bytes"
        headers = {
            "X-API-Key": api_key,
            "Cartesia-Version": "2024-06-10",
            "Content-Type": "application/json",
        }
        payload = {
            "model_id": "sonic-3",
            "transcript": text,
            "voice": {"mode": "id", "id": voice_id},
            "output_format": {
                "container": "wav",
                "encoding": "pcm_s16le",
                "sample_rate": 24000,
            },
        }
        res = requests.post(url, headers=headers, json=payload, timeout=8)
        if res.status_code == 200:
            return res.content
        raise RuntimeError(f"Cartesia TTS failed: {res.status_code} - {res.text}")

    @classmethod
    def upload_to_s3(cls, audio_bytes: bytes, file_name: str) -> str:
        s3_key = f"tts/{file_name}.wav"
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=audio_bytes,
            ContentType="audio/wav"
        )
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": s3_key},
            ExpiresIn=3600
        )
        return url
