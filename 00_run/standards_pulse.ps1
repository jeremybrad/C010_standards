# C010_standards - Standards Pulse (Windows)
# Right-click → "Run with PowerShell" to generate fresh Standards inventory exports
#
# Outputs: 70_evidence\exports\Standards_Pulse.xlsx, Standards_Inventory.csv
#          20_receipts\<date>_standards_pulse.md
#
# Note: If you get "execution policy" error, run once as admin:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

$ErrorActionPreference = "Stop"

# Navigate to repo root (parent of 00_run/)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
Set-Location $RepoRoot

Write-Host "=============================================="
Write-Host "C010_standards - Standards Pulse"
Write-Host "=============================================="
Write-Host "Repo: $RepoRoot"
Write-Host ""

# Find Python (prefer venv if exists)
$Python = $null
if (Test-Path ".venv_gui_win\Scripts\python.exe") {
    $Python = ".venv_gui_win\Scripts\python.exe"
} elseif (Test-Path ".venv\Scripts\python.exe") {
    $Python = ".venv\Scripts\python.exe"
} elseif (Test-Path "venv\Scripts\python.exe") {
    $Python = "venv\Scripts\python.exe"
} else {
    $Python = "python"
}

Write-Host "Using Python: $Python"
Write-Host ""

# Ensure output directories exist
New-Item -ItemType Directory -Force -Path "70_evidence\exports" | Out-Null
New-Item -ItemType Directory -Force -Path "20_receipts" | Out-Null

# Run the export script
Write-Host "--- Running export_standards_pulse.py ---"
& $Python tools/export_standards_pulse.py

Write-Host ""
Write-Host "=============================================="
Write-Host "RECEIPT"
Write-Host "=============================================="
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""
Write-Host "Output files:"
Get-ChildItem 70_evidence\exports\Standards_*.xlsx, 70_evidence\exports\Standards_*.csv -ErrorAction SilentlyContinue | ForEach-Object {
    $size = "{0:N1} KB" -f ($_.Length / 1KB)
    Write-Host "  $($_.Name) ($size)"
}
Write-Host ""
Write-Host "Receipt files:"
$receipts = Get-ChildItem 20_receipts\*_standards_pulse.md -ErrorAction SilentlyContinue | Sort-Object LastWriteTime | Select-Object -Last 1
if ($receipts) {
    $size = "{0:N1} KB" -f ($receipts.Length / 1KB)
    Write-Host "  $($receipts.Name) ($size)"
}
Write-Host ""
Write-Host "Done! Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
