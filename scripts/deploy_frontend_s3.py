import boto3
import os
import mimetypes
import json
from dotenv import load_dotenv

load_dotenv(override=True)

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
BUCKET_NAME = "janai-web-hosting-2026"  # Must be globally unique

s3_client = boto3.client("s3", region_name=AWS_REGION)

def deploy():
    print(f"[*] Creating S3 bucket: {BUCKET_NAME} in {AWS_REGION}...")
    try:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print("  [OK] Bucket created successfully.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print("  [OK] Bucket already owned by you.")
    except Exception as e:
        print(f"  [!] Error creating bucket: {e}")
        return

    # Disable Block Public Access
    print("[*] Disabling Public Access Blocks...")
    try:
        s3_client.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print("  [OK] Public access blocks disabled.")
    except Exception as e:
        print(f"  [!] Error disabling public access block: {e}")

    # Set Bucket Policy
    print("[*] Setting bucket policy for public read access...")
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
            }
        ]
    }
    try:
        s3_client.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=json.dumps(bucket_policy)
        )
        print("  [OK] Bucket policy applied.")
    except Exception as e:
        print(f"  [!] Error applying bucket policy: {e}")

    # Enable Static Website Hosting
    print("[*] Enabling static website hosting...")
    try:
        s3_client.put_bucket_website(
            Bucket=BUCKET_NAME,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': 'index.html'}  # Redirect to index.html for SPA routing fallback
            }
        )
        print("  [OK] Static website hosting enabled.")
    except Exception as e:
        print(f"  [!] Error enabling website hosting: {e}")

    # Upload files
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "website", "dist"))
    if not os.path.exists(dist_dir):
        print(f"  [!] Build directory does not exist: {dist_dir}. Please run build first.")
        return

    print(f"[*] Uploading files from {dist_dir} to s3://{BUCKET_NAME}...")
    uploaded_count = 0
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, dist_dir).replace("\\", "/")
            
            # Guess mime-type
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                if file.endswith(".glb"):
                    content_type = "model/gltf-binary"
                else:
                    content_type = "application/octet-stream"

            try:
                s3_client.upload_file(
                    local_path,
                    BUCKET_NAME,
                    relative_path,
                    ExtraArgs={
                        "ContentType": content_type,
                        "CacheControl": "public, max-age=31536000, immutable" if "assets/" in relative_path else "no-cache"
                    }
                )
                uploaded_count += 1
            except Exception as e:
                print(f"  [!] Error uploading {relative_path}: {e}")

    print(f"  [OK] Uploaded {uploaded_count} files.")
    website_url = f"http://{BUCKET_NAME}.s3-website-{AWS_REGION}.amazonaws.com"
    print("\n" + "="*60)
    print("FRONTEND DEPLOYED TO AWS S3!")
    print(f"URL: {website_url}")
    print("="*60)

if __name__ == "__main__":
    deploy()
