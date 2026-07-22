$ErrorActionPreference = 'Stop'

function Fail($message) {
  Write-Host "FAILED: $message" -ForegroundColor Red
  exit 1
}

Write-Host "Mission GroundWork local automation install" -ForegroundColor Cyan

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Fail "Docker CLI is not installed or not on PATH. Install/open Docker Desktop, then rerun this script."
}

try { docker info | Out-Null } catch { Fail "Docker Desktop is installed but the Docker engine is not running." }

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Test-Path '.env')) {
  $keyBytes = New-Object byte[] 32
  [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($keyBytes)
  $key = [Convert]::ToBase64String($keyBytes)
  $passwordBytes = New-Object byte[] 24
  [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($passwordBytes)
  $password = [Convert]::ToBase64String($passwordBytes).Replace('/','_').Replace('+','-')
  (Get-Content '.env.example' -Raw).Replace('replace-with-a-long-random-string', $key).Replace('replace-with-a-long-random-password', $password) | Set-Content '.env' -Encoding utf8
  Write-Host "Created automation/.env with local random secrets."
}

Write-Host "Validating Compose..."
docker compose config --quiet

Write-Host "Pulling core images..."
docker compose pull n8n baserow

Write-Host "Starting n8n and Baserow..."
docker compose up -d n8n baserow

function Wait-Http($name, $url, $seconds) {
  $deadline = (Get-Date).AddSeconds($seconds)
  do {
    try {
      $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
      if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
        Write-Host "$name responded at $url" -ForegroundColor Green
        return
      }
    } catch {}
    Start-Sleep -Seconds 3
  } while ((Get-Date) -lt $deadline)

  docker compose ps
  docker compose logs --tail=100 $name
  Fail "$name did not respond at $url within $seconds seconds."
}

Wait-Http 'n8n' 'http://localhost:5678/healthz' 180
Wait-Http 'baserow' 'http://localhost:8000/api/_health/' 300

Write-Host "Generating seven n8n workflow exports..."
if (Get-Command python -ErrorAction SilentlyContinue) {
  python scripts/build_n8n_workflows.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  py scripts/build_n8n_workflows.py
} else {
  Write-Warning "Python is unavailable; workflow exports already committed in automation/n8n/workflows."
}

$workflowCount = (Get-ChildItem 'n8n/workflows/workflow_*.json').Count
if ($workflowCount -ne 7) { Fail "Expected 7 workflow exports, found $workflowCount." }

Write-Host "INSTALL VERIFIED" -ForegroundColor Green
Write-Host "n8n: http://localhost:5678"
Write-Host "Baserow: http://localhost:8000"
Write-Host "Next: import automation/n8n/workflows/*.json into n8n and authorize Google credentials."

docker compose ps
