$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  throw "Backend virtual environment not found at .venv. Run setup first."
}

& ".\.venv\Scripts\python.exe" -m pytest
