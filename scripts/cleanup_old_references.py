#!/usr/bin/env python3
"""
JanAI — Old Branding → JanAI Cleanup Script
==========================================
Scans DynamoDB tables and S3 for any remaining old references
and replaces them with 'JanAI'. Also clears cached TTS audio.

Run ONCE after deploying the updated Lambda:
    python scripts/cleanup_old_references.py
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)

AWS_REGION  = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET   = os.environ.get("S3_DOCUMENTS_BUCKET", "janai-documents-2026")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
s3       = boto3.client("s3", region_name=AWS_REGION)

KNOWLEDGE_TABLE      = os.environ.get("DYNAMODB_KNOWLEDGE_TABLE", "janai_knowledge")
CALLS_TABLE          = os.environ.get("DYNAMODB_CALLS_TABLE", "janai_calls")
PHONE_PROFILES_TABLE = os.environ.get("DYNAMODB_PHONE_PROFILES_TABLE", "janai_phone_profiles")

REPLACEMENTS = [
    ("VaaniSeva", "JanAI"),
    ("vaaniseva", "janai"),
    ("VAANISEVA", "JANAI"),
    ("Vaani Seva", "JanAI"),
    ("vaani seva", "janai"),
    ("vaani-seva", "janai"),
]


def replace_vaaniseva(text: str) -> str:
    if not isinstance(text, str):
        return text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def fix_item_value(value):
    """Recursively fix VaaniSeva in strings, dicts, and lists."""
    if isinstance(value, str):
        return replace_vaaniseva(value)
    elif isinstance(value, dict):
        return {k: fix_item_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [fix_item_value(v) for v in value]
    return value


def has_vaaniseva(value) -> bool:
    """Recursively check if VaaniSeva exists anywhere in the value."""
    text = json.dumps(value, default=str) if not isinstance(value, str) else value
    return any(old.lower() in text.lower() for old, _ in REPLACEMENTS)


# ── 1. Knowledge Table ──────────────────────────────────────────
def clean_knowledge_table():
    print(f"[*] Scanning knowledge table: {KNOWLEDGE_TABLE}")
    table   = dynamodb.Table(KNOWLEDGE_TABLE)
    fixed   = 0
    scanned = 0

    paginator_args = {}
    while True:
        resp  = table.scan(**paginator_args)
        items = resp.get("Items", [])
        scanned += len(items)

        for item in items:
            item_json = json.dumps(item, default=str)
            if not has_vaaniseva(item_json):
                continue

            fields_to_fix = ["text_hi", "text_en", "text_mr", "text_ta", "title", "description",
                              "name_hi", "name_en", "personality", "greeting_hi", "greeting_en"]
            updates = {}
            for field in fields_to_fix:
                if field in item and has_vaaniseva(item[field]):
                    updates[field] = fix_item_value(item[field])

            if updates:
                key = {k: item[k] for k in ["scheme_id", "section_id"] if k in item}
                if not key:
                    print(f"  [!] Cannot determine key for item: {list(item.keys())[:5]}")
                    continue

                expr_parts, expr_vals, expr_names = [], {}, {}
                for i, (k, v) in enumerate(updates.items()):
                    an, av = f"#f{i}", f":v{i}"
                    expr_parts.append(f"{an} = {av}")
                    expr_names[an] = k
                    expr_vals[av]  = v

                table.update_item(
                    Key=key,
                    UpdateExpression="SET " + ", ".join(expr_parts),
                    ExpressionAttributeNames=expr_names,
                    ExpressionAttributeValues=expr_vals,
                )
                fixed += 1
                print(f"  [OK] Fixed: {item.get('scheme_id','?')} / {item.get('section_id','?')}")

        if "LastEvaluatedKey" not in resp:
            break
        paginator_args["ExclusiveStartKey"] = resp["LastEvaluatedKey"]

    print(f"  Scanned {scanned} items, fixed {fixed}")


# ── 2. Calls Table (conversation history) ──────────────────────
def clean_calls_table():
    print(f"[*] Scanning calls table: {CALLS_TABLE}")
    table   = dynamodb.Table(CALLS_TABLE)
    fixed   = 0
    scanned = 0

    paginator_args = {}
    while True:
        resp  = table.scan(**paginator_args)
        items = resp.get("Items", [])
        scanned += len(items)

        for item in items:
            item_json = json.dumps(item, default=str)
            if not has_vaaniseva(item_json):
                continue

            key = {}
            if "call_id" in item:
                key["call_id"] = item["call_id"]
            if "timestamp" in item:
                key["timestamp"] = item["timestamp"]
            if not key:
                continue

            updates = {}
            for field in ["conversation_history", "status", "source"]:
                if field in item and has_vaaniseva(item[field]):
                    updates[field] = fix_item_value(item[field])

            if updates:
                expr_parts, expr_vals, expr_names = [], {}, {}
                for i, (k, v) in enumerate(updates.items()):
                    an, av = f"#f{i}", f":v{i}"
                    expr_parts.append(f"{an} = {av}")
                    expr_names[an] = k
                    expr_vals[av]  = v

                table.update_item(
                    Key=key,
                    UpdateExpression="SET " + ", ".join(expr_parts),
                    ExpressionAttributeNames=expr_names,
                    ExpressionAttributeValues=expr_vals,
                )
                fixed += 1

        if "LastEvaluatedKey" not in resp:
            break
        paginator_args["ExclusiveStartKey"] = resp["LastEvaluatedKey"]

    print(f"  Scanned {scanned} items, fixed {fixed}")


# ── 3. Phone Profiles Table ─────────────────────────────────────
def clean_phone_profiles_table():
    print(f"[*] Scanning phone profiles: {PHONE_PROFILES_TABLE}")
    try:
        table   = dynamodb.Table(PHONE_PROFILES_TABLE)
        fixed   = 0
        scanned = 0

        paginator_args = {}
        while True:
            resp  = table.scan(**paginator_args)
            items = resp.get("Items", [])
            scanned += len(items)

            for item in items:
                item_json = json.dumps(item, default=str)
                if not has_vaaniseva(item_json):
                    continue

                key = {"phone_hash": item["phone_hash"]}
                updates = {k: fix_item_value(v) for k, v in item.items()
                           if k != "phone_hash" and has_vaaniseva(v)}

                if updates:
                    expr_parts, expr_vals, expr_names = [], {}, {}
                    for i, (k, v) in enumerate(updates.items()):
                        an, av = f"#f{i}", f":v{i}"
                        expr_parts.append(f"{an} = {av}")
                        expr_names[an] = k
                        expr_vals[av]  = v

                    table.update_item(
                        Key=key,
                        UpdateExpression="SET " + ", ".join(expr_parts),
                        ExpressionAttributeNames=expr_names,
                        ExpressionAttributeValues=expr_vals,
                    )
                    fixed += 1

            if "LastEvaluatedKey" not in resp:
                break
            paginator_args["ExclusiveStartKey"] = resp["LastEvaluatedKey"]

        print(f"  Scanned {scanned} items, fixed {fixed}")
    except Exception as e:
        print(f"  [!] Phone profiles table error (may not exist): {e}")


# ── 4. S3 TTS Cache Cleanup ─────────────────────────────────────
def clean_s3_tts_cache():
    print(f"[*] Clearing S3 TTS cache: s3://{S3_BUCKET}/tts/")
    try:
        paginator = s3.get_paginator("list_objects_v2")
        deleted   = 0

        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix="tts/"):
            objects = page.get("Contents", [])
            if not objects:
                continue
            keys = [{"Key": obj["Key"]} for obj in objects]
            s3.delete_objects(Bucket=S3_BUCKET, Delete={"Objects": keys})
            deleted += len(keys)

        print(f"[OK] Deleted {deleted} cached TTS audio files")
    except Exception as e:
        print(f"  [!] S3 cleanup error: {e}")


# ── 5. Verify Lambda env var ────────────────────────────────────
def verify_lambda_env():
    print(f"[*] Verifying Lambda environment variables...")
    try:
        lam  = boto3.client("lambda", region_name=AWS_REGION)
        conf = lam.get_function_configuration(FunctionName="janai-call-handler")
        env  = conf.get("Environment", {}).get("Variables", {})
        api_url = env.get("API_BASE_URL", "NOT SET")
        if "7hrrqf2fol" in api_url:
            print(f"  ✅ API_BASE_URL = {api_url}")
        else:
            print(f"  ❌ API_BASE_URL = {api_url}  ← still wrong!")
            print(f"     Run: python scripts/deploy.py  to fix the Lambda env var")
    except Exception as e:
        print(f"  ⚠  Could not verify Lambda env: {e}")


if __name__ == "__main__":
    print("=" * 55)
    print("JanAI — Old Branding Cleanup")
    print("=" * 55)

    clean_knowledge_table()
    clean_calls_table()
    clean_phone_profiles_table()
    clean_s3_tts_cache()
    verify_lambda_env()

    print("\n" + "=" * 55)
    print("✅ Cleanup complete!")
    print("=" * 55)
