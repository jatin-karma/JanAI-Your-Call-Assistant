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
    
    # Upload
    Write-Host "  Uploading to Lambda..." -ForegroundColor Yellow
    $result = aws lambda update-function-code `
        --function-name $FunctionName `
        --zip-file "fileb://$((Resolve-Path $zipPath).Path)" `
        --region $REGION `
        --query "LastModified" --output text
    
    Write-Host "  Waiting for activation..."
    aws lambda wait function-updated --function-name $FunctionName --region $REGION
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
