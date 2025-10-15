param(
  [switch]$Clean,
  [string]$Spec = "pyinstaller.spec"
)

$ErrorActionPreference = 'Stop'

Write-Host "Setting up venv..."
python -m venv .venv
.\.venv\Scripts\pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

if ($Clean) {
  Write-Host "Cleaning dist and build..."
  Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue | Out-Null
}

Write-Host "Running PyInstaller..."
.\.venv\Scripts\pyinstaller $Spec --noconfirm

Write-Host "Copying plugins directory if present..."
if (Test-Path .\docs\plugins) {
  New-Item -ItemType Directory -Force -Path .\dist\HungerBens\plugins | Out-Null
  Copy-Item -Recurse -Force .\docs\plugins\* .\dist\HungerBens\plugins\
}

Write-Host "Done. Output at dist/HungerBens"
