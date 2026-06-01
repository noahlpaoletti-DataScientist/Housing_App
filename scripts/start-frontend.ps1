$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $root "frontend")

$env:Path = "C:\Program Files\nodejs;$env:Path"

if (-not (Test-Path ".\node_modules")) {
  throw "Frontend dependencies are not installed. Run npm install in frontend first."
}

& "C:\Program Files\nodejs\npm.cmd" run dev -- --host 127.0.0.1 --port 5173
