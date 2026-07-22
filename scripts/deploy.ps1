# JanAI Lambda Deploy Script
# Usage: powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1
# Deploys both Lambdas from local venv packages — no pip install needed

param(
    [switch]$CallHandler,
    [switch]$WebAgent,
    [switch]$All
)

if (-not $CallHandler -and -not $WebAgent) { $All = $true }

$REGION = "us-east-1"
$SP = "venv\Lib\site-packages"

function Deploy-Lambda {
    param($FunctionName, $HandlerSrc, $ExtraSrc = @())
    
    Write-Host "`n=== Deploying $FunctionName ===" -ForegroundColor Cyan
    
    # Clean build dir
    if (Test-Path "build\$FunctionName") { Remove-Item "build\$FunctionName" -Recurse -Force }
    New-Item -ItemType Directory -Path "build\$FunctionName" | Out-Null
    
    # Copy handler(s)
    Copy-Item $HandlerSrc "build\$FunctionName\" -Force
    foreach ($extra in $ExtraSrc) {
        if (Test-Path $extra) { Copy-Item $extra "build\$FunctionName\" -Force }
    }
    # Copy modular services folder if present
    $servicesPath = Join-Path (Split-Path $HandlerSrc -Parent) "services"
    if (Test-Path $servicesPath) {
        Copy-Item $servicesPath "build\$FunctionName\" -Recurse -Force
        Write-Host "  Copied services/ module package." -ForegroundColor Cyan
    }
    
    # Copy pure-Python packages from venv (already proven to work on Lambda)
    $pkgsNeeded = @("requests", "certifi", "urllib3", "charset_normalizer", "idna",
                    "twilio", "jwt", "PyJWT")
    foreach ($pkg in $pkgsNeeded) {
        $path = Join-Path $SP $pkg
        if (Test-Path $path) {
            Copy-Item $path "build\$FunctionName\" -Recurse -Force
        }
    }
    # Also copy dist-info folders for the key packages
    Get-ChildItem $SP | Where-Object { $_.Name -match "^(twilio|pyjwt|requests|urllib3|certifi|charset_normalizer|idna).*dist-info$" } | ForEach-Object {
        Copy-Item $_.FullName "build\$FunctionName\" -Recurse -Force
    }
    
    # Zip it
    $zipPath = "$FunctionName-deploy.zip"
    Compress-Archive -Path "build\$FunctionName\*" -DestinationPath $zipPath -Force
    $sizeMB = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
    Write-Host "  Package size: $sizeMB MB" -ForegroundColor Green
    
    # Upload via S3 bucket (reliable multipart chunking, no connection drops)
    $s3Bucket = "janai-documents-2026"
    $s3Key = "deployments/$FunctionName-deploy.zip"
    Write-Host "  Uploading zip to S3 (s3://$s3Bucket/$s3Key)..." -ForegroundColor Yellow
    aws s3 cp $zipPath "s3://$s3Bucket/$s3Key" --region $REGION
    
    Write-Host "  Updating Lambda code from S3..." -ForegroundColor Yellow
    $result = aws lambda update-function-code `
        --function-name $FunctionName `
        --s3-bucket $s3Bucket `
        --s3-key $s3Key `
        --region $REGION `
        --query "LastModified" --output text
    
    Write-Host "  Waiting for activation..."
    aws lambda wait function-updated --function-name $FunctionName --region $REGION
    
    Write-Host "  Updating Lambda environment variables..." -ForegroundColor Yellow
    python scripts/update_env_vars.py $FunctionName
    
    Write-Host "  DEPLOYED at $result" -ForegroundColor Green
}

# Deploy call handler
if ($CallHandler -or $All) {
    Deploy-Lambda `
        -FunctionName "janai-call-handler" `
        -HandlerSrc "lambdas\call_handler\handler.py" `
        -ExtraSrc @("lambdas\call_handler\connect_handler.py")
}

# Deploy web agent  
if ($WebAgent -or $All) {
    Deploy-Lambda `
        -FunctionName "janai-web-agent" `
        -HandlerSrc "lambdas\web_agent\handler.py"
}

Write-Host "`n=== All deployments complete! ===" -ForegroundColor Cyan
Write-Host "Smoke test: Invoke-WebRequest -Uri 'https://7hrrqf2fol.execute-api.us-east-1.amazonaws.com/prod/voice/incoming' -Method POST -Body 'CallSid=test&lang=hi&voice=arya&From=%2B910000000000' -ContentType 'application/x-www-form-urlencoded'"
