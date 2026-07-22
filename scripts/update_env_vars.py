import boto3
import os
import sys
from dotenv import load_dotenv

# Load .env relative to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
lambda_client = boto3.client("lambda", region_name=AWS_REGION)

env_vars = {
    "DYNAMODB_CALLS_TABLE":     os.environ.get("DYNAMODB_CALLS_TABLE", "janai_calls"),
    "DYNAMODB_KNOWLEDGE_TABLE": os.environ.get("DYNAMODB_KNOWLEDGE_TABLE", "janai_knowledge"),
    "DYNAMODB_VECTORS_TABLE":   os.environ.get("DYNAMODB_VECTORS_TABLE", "janai_vectors"),
    "DYNAMODB_USERS_TABLE":          os.environ.get("DYNAMODB_USERS_TABLE", "janai_users"),
    "DYNAMODB_PHONE_PROFILES_TABLE": os.environ.get("DYNAMODB_PHONE_PROFILES_TABLE", "janai-phone-profiles"),
    "S3_DOCUMENTS_BUCKET":      os.environ.get("S3_DOCUMENTS_BUCKET", "janai-documents-2026"),
    "BEDROCK_MODEL_ID":         os.environ.get("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0"),
    "BEDROCK_EMBEDDING_MODEL_ID": os.environ.get("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    "TWILIO_ACCOUNT_SID":       os.environ.get("TWILIO_ACCOUNT_SID", ""),
    "TWILIO_AUTH_TOKEN":        os.environ.get("TWILIO_AUTH_TOKEN", ""),
    "TWILIO_PHONE_NUMBER":      os.environ.get("TWILIO_PHONE_NUMBER", "").strip(),
    "TWILIO_API_KEY_SID":       os.environ.get("TWILIO_API_KEY_SID", ""),
    "TWILIO_API_KEY_SECRET":    os.environ.get("TWILIO_API_KEY_SECRET", ""),
    "TWILIO_TWIML_APP_SID":     os.environ.get("TWILIO_TWIML_APP_SID", ""),
    "API_BASE_URL":             os.environ.get("API_BASE_URL", ""),
    "SARVAM_API_KEY":            os.environ.get("SARVAM_API_KEY", "").strip(),
    "OPENAI_API_KEY":            os.environ.get("OPENAI_API_KEY", ""),
    "LLM_PROVIDER":             os.environ.get("LLM_PROVIDER", "bedrock"),
    "JWT_SECRET":                os.environ.get("JWT_SECRET", ""),
    "DATA_GOV_API_KEY":          os.environ.get("DATA_GOV_API_KEY", "").strip(),
    "CARTESIA_API_KEY":          os.environ.get("CARTESIA_API_KEY", ""),
    "TTS_PROVIDER":              os.environ.get("TTS_PROVIDER", "sarvam"),
    "LOG_LEVEL":                "INFO",
}

def update_lambda_config(function_name):
    print(f"Updating configuration for Lambda '{function_name}'...")
    try:
        res = lambda_client.update_function_configuration(
            FunctionName=function_name,
            Environment={"Variables": env_vars},
            Timeout=30,
            MemorySize=1024
        )
        print(f"  [OK] Updated successfully. CodeSize: {res.get('CodeSize')}")
    except Exception as e:
        print(f"  [ERROR] Failed for '{function_name}': {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_lambda_config(sys.argv[1])
    else:
        update_lambda_config("janai-call-handler")
        update_lambda_config("janai-web-agent")
