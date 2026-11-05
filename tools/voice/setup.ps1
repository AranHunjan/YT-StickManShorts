# One-time setup for the voice bake-off on Windows with an NVIDIA GPU.
# From the repo root, in PowerShell:
#   powershell -ExecutionPolicy Bypass -File tools\voice\setup.ps1
#
# Creates three separate Python environments under tools\voice\.venvs
# (the engines' dependencies conflict, so they cannot share one).

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvs = Join-Path $here ".venvs"
# CUDA 12.4 builds of PyTorch 2.6 support the RTX 20-series (Turing) and newer.
$torchIndex = "https://download.pytorch.org/whl/cu124"

function Invoke-Step {
    param([string]$Label, [scriptblock]$Block)
    Write-Host "`n=== $Label ===" -ForegroundColor Cyan
    & $Block
    if ($LASTEXITCODE -ne 0) { throw "Step failed: $Label" }
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Invoke-Step "Install uv (Python and package manager)" {
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    }
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

function New-Env([string]$name) {
    $dir = Join-Path $venvs $name
    Invoke-Step "Create environment: $name (Python 3.11)" { uv venv --python 3.11 $dir }
    return (Join-Path $dir "Scripts\python.exe")
}

$py = New-Env "kokoro"
Invoke-Step "kokoro: PyTorch (CUDA)" { uv pip install --python $py torch==2.6.0 --index-url $torchIndex }
Invoke-Step "kokoro: packages" {
    uv pip install --python $py kokoro==0.9.4 soundfile `
        "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
}

$py = New-Env "chatterbox"
Invoke-Step "chatterbox: PyTorch (CUDA)" { uv pip install --python $py torch==2.6.0 torchaudio==2.6.0 --index-url $torchIndex }
# setuptools<81: Chatterbox's watermark library still imports pkg_resources,
# which uv environments don't include and newer setuptools no longer ship.
Invoke-Step "chatterbox: packages" { uv pip install --python $py chatterbox-tts==0.1.7 "setuptools<81" faster-whisper }

$py = New-Env "qwen"
Invoke-Step "qwen: PyTorch (CUDA)" { uv pip install --python $py torch==2.6.0 torchaudio==2.6.0 --index-url $torchIndex }
Invoke-Step "qwen: packages" { uv pip install --python $py qwen-tts==0.1.1 soundfile }

Invoke-Step "GPU check" {
    & (Join-Path $venvs "chatterbox\Scripts\python.exe") -c "import torch; ok = torch.cuda.is_available(); print('CUDA available:', ok, torch.cuda.get_device_name(0) if ok else '(no GPU found: update the NVIDIA driver)')"
}
Write-Host "`nSetup finished. Next: powershell -ExecutionPolicy Bypass -File tools\voice\run_bakeoff.ps1" -ForegroundColor Green
