# Runs every engine on the same lines, then builds one comparison file per engine.
# From the repo root, in PowerShell:
#   powershell -ExecutionPolicy Bypass -File tools\voice\run_bakeoff.ps1
# The first run downloads the models (roughly 10 GB in total) into
# %USERPROFILE%\.cache\huggingface. Later runs are fast.

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$v = Join-Path $here ".venvs"
$script = Join-Path $here "bakeoff.py"
$refs = Join-Path $here "..\..\out\voice-bakeoff\refs"

function Run([string]$envName, [string[]]$scriptArgs) {
    $py = Join-Path $v "$envName\Scripts\python.exe"
    Write-Host "`n=== $envName $($scriptArgs -join ' ') ===" -ForegroundColor Cyan
    & $py $script @scriptArgs
    if ($LASTEXITCODE -ne 0) { throw "Failed: $envName $($scriptArgs -join ' ')" }
}

# Start clean so the "built-in voice" runs really use the built-in voice.
if (Test-Path $refs) { Remove-Item -Recurse -Force $refs }

Run "kokoro"     @("--engine", "kokoro")
Run "chatterbox" @("--engine", "chatterbox")   # built-in voice
Run "chatterbox" @("--engine", "turbo")        # built-in voice
Run "qwen"       @("--engine", "qwen")         # designs Kip and Dex, writes refs\
Run "chatterbox" @("--engine", "chatterbox")   # now clones the designed voices
Run "chatterbox" @("--engine", "turbo")        # now clones the designed voices
Run "chatterbox" @("--compare")

Write-Host "`nDone. Listen to the files in out\voice-bakeoff\compare\" -ForegroundColor Green
