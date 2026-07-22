$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logPath = Join-Path $scriptDir 'install-local.log'
Start-Transcript -Path $logPath -Append | Out-Null

function Fail([string]$message) {
  Write-Host "FAILED: $message" -ForegroundColor Red
  Write-Host "Log: $logPath" -ForegroundColor Yellow
  Stop-Transcript | Out-Null
  exit 1
}

function Run-Native([string]$label, [string]$file, [string[]]$arguments) {
  Write-Host "[$label] $file $($arguments -join ' ')" -ForegroundColor Cyan
  & $file @arguments
  if ($LASTEXITCODE -ne 0) {
    Fail "$label exited with code $LASTEXITCODE."
  }
}

function Test-DockerEngine([int]$timeoutSeconds = 30) {
  Write-Host "[docker-engine] Checking Docker engine with ${timeoutSeconds}s timeout..." -ForegroundColor Cyan
  $job = Start-Job -ScriptBlock {
    $output = & docker info 2>&1
    [pscustomobject]@{ ExitCode = $LASTEXITCODE; Output = ($output -join [Environment]::NewLine) }
  }
  try {
    if (-not (Wait-Job -Job $job -Timeout $timeoutSeconds)) {
      Stop-Job $job -Force -ErrorAction SilentlyContinue
      Fail "Docker CLI responded, but 'docker info' timed out. Open Docker Desktop and wait until the engine says Running."
    }
    $result = Receive-Job $job
    if ($result.ExitCode -ne 0) {
      Write-Host $result.Output
      Fail "Docker engine is unavailable. Open Docker Desktop and confirm Linux containers are running."
    }
  } finally {
    Remove-Job $job -Force -ErrorAction SilentlyContinue
  }
  Write-Host "[docker-engine] Docker engine is running." -ForegroundColor Green
}

try {
  Write-Host "Mission GroundWork local automation install" -ForegroundColor Cyan
  Write-Host "Script: $PSCommandPath"
  Write-Host "Log: $logPath"

  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Fail "Docker CLI is not installed or not on PATH. Install/open Docker Desktop, then rerun this script."
  }

  Test-DockerEngine 30
  Set-Location $scriptDir
  Write-Host "[working-directory] $scriptDir" -ForegroundColor Green

  if (-not (Test-Path '.env.example')) {
    Fail "Missing .env.example in $scriptDir. Pull the latest main branch and rerun."
  }
  if (-not (Test-Path 'docker-compose.yml')) {
    Fail "Missing docker-compose.yml in $scriptDir. Pull the latest main branch and rerun."
  }

  if (-not (Test-Path '.env')) {
    Write-Host "[environment] Creating local random secrets..." -ForegroundColor Cyan
    $keyBytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($keyBytes)
    $key = [Convert]::ToBase64String($keyBytes)
    $passwordBytes = New-Object byte[] 24
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($passwordBytes)
    $password = [Convert]::ToBase64String($passwordBytes).Replace('/','_').Replace('+','-')
    (Get-Content '.env.example' -Raw).Replace('replace-with-a-long-random-string', $key).Replace('replace-with-a-long-random-password', $password) | Set-Content '.env' -Encoding utf8
    Write-Host "[environment] Created automation/.env." -ForegroundColor Green
  } else {
    Write-Host "[environment] Reusing existing automation/.env." -ForegroundColor Green
  }

  Run-Native 'compose-validate' 'docker' @('compose','config','--quiet')
  Run-Native 'compose-pull' 'docker' @('compose','pull','n8n','baserow')
  Run-Native 'compose-start' 'docker' @('compose','up','-d','n8n','baserow')

  function Wait-Http([string]$name, [string]$url, [int]$seconds) {
    Write-Host "[health:$name] Waiting for $url for up to $seconds seconds..." -ForegroundColor Cyan
    $deadline = (Get-Date).AddSeconds($seconds)
    do {
      try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
          Write-Host "[health:$name] Responded with HTTP $($response.StatusCode)." -ForegroundColor Green
          return
        }
      } catch {
        Write-Host "." -NoNewline
      }
      Start-Sleep -Seconds 3
    } while ((Get-Date) -lt $deadline)

    Write-Host ""
    & docker compose ps
    & docker compose logs --tail=100 $name
    Fail "$name did not respond at $url within $seconds seconds."
  }

  Wait-Http 'n8n' 'http://localhost:5678/healthz' 180
  Wait-Http 'baserow' 'http://localhost:8000/api/_health/' 300

  Write-Host "[workflows] Generating seven n8n workflow exports..." -ForegroundColor Cyan
  if (Get-Command python -ErrorAction SilentlyContinue) {
    Run-Native 'workflow-build' 'python' @('scripts/build_n8n_workflows.py')
  } elseif (Get-Command py -ErrorAction SilentlyContinue) {
    Run-Native 'workflow-build' 'py' @('scripts/build_n8n_workflows.py')
  } else {
    Fail "Python is unavailable and workflow exports cannot be generated. Install Python or run the committed workflow generator elsewhere."
  }

  $workflowFiles = @(Get-ChildItem 'n8n/workflows/workflow_*.json' -ErrorAction SilentlyContinue)
  if ($workflowFiles.Count -ne 7) {
    Fail "Expected 7 workflow exports, found $($workflowFiles.Count)."
  }

  Write-Host "INSTALL VERIFIED" -ForegroundColor Green
  Write-Host "n8n: http://localhost:5678"
  Write-Host "Baserow: http://localhost:8000"
  Write-Host "Workflow files: $($workflowFiles.Count)"
  & docker compose ps
  Stop-Transcript | Out-Null
  exit 0
} catch {
  Fail $_.Exception.Message
}
