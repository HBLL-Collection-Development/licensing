Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

python -m pip install --upgrade pip
pip install -r requirements.txt -ErrorAction SilentlyContinue
pip install build -ErrorAction SilentlyContinue

if (Test-Path -Path dist) { Remove-Item -Recurse -Force dist }
python -m build --outdir dist

Write-Host "Built artifacts in dist\"
Get-ChildItem -Path dist -Recurse | ForEach-Object { Write-Host $_.FullName }
