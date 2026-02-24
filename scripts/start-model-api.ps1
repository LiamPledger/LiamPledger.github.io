param(
  [string]$Host = "127.0.0.1",
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$apiDir = Join-Path $repoRoot "api"
$venvDir = Join-Path $apiDir ".venv"
$pythonExe = Join-Path $venvDir "Scripts\python.exe"
$hasPython = [bool](Get-Command python -ErrorAction SilentlyContinue)
$hasPy = [bool](Get-Command py -ErrorAction SilentlyContinue)

if (-not (Test-Path $pythonExe)) {
  if ($hasPython) {
    & python -m venv $venvDir
  } elseif ($hasPy) {
    & py -3 -m venv $venvDir
  } else {
    throw "Python is not available in PATH. Install Python 3 first."
  }
}

& $pythonExe -m pip install -r (Join-Path $apiDir "requirements.txt")
& $pythonExe -m uvicorn main:app --host $Host --port $Port --app-dir $apiDir
