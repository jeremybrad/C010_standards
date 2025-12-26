# audit_syncedprojects.ps1 - Folder Structure Audit Launcher
# Windows: Right-click -> Run with PowerShell
#
# Audits all repos in ~/SyncedProjects for Betty Protocol compliance.
# Produces CSV output for pivoting compliance across repos.
#
# Note: Requires Git Bash or WSL to run the underlying bash script.

$ErrorActionPreference = "Stop"

# Navigate to repo root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
Set-Location $RepoRoot

Write-Host "=============================================="
Write-Host "C010_standards - Folder Structure Audit"
Write-Host "=============================================="
Write-Host "Repo: $RepoRoot"
Write-Host ""

# Default workspace
$Workspace = if ($args[0]) { $args[0] } else { "$env:USERPROFILE\SyncedProjects" }

Write-Host "Auditing: $Workspace"
Write-Host ""

# Check for Git Bash
$GitBash = Get-Command "bash" -ErrorAction SilentlyContinue
if (-not $GitBash) {
    Write-Host "ERROR: bash not found. Please install Git for Windows." -ForegroundColor Red
    Write-Host "Download: https://git-scm.com/download/win"
    Write-Host ""
    Write-Host "Press any key to close..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Run the audit script via bash
try {
    bash scripts/audit_folder_structure.sh $Workspace
    $ExitCode = $LASTEXITCODE
} catch {
    Write-Host "ERROR: Failed to run audit script" -ForegroundColor Red
    Write-Host $_.Exception.Message
    $ExitCode = 1
}

Write-Host ""
Write-Host "=============================================="
Write-Host "OUTPUT FILES"
Write-Host "=============================================="
Write-Host ""

# Show CSV location
$CsvLatest = Join-Path $RepoRoot "70_evidence\exports\folder_structure_audit_latest.csv"
if (Test-Path $CsvLatest) {
    Write-Host "CSV (latest): $CsvLatest"
    Write-Host ""
    Write-Host "Preview (first 5 rows):"
    Get-Content $CsvLatest | Select-Object -First 6 | ForEach-Object { Write-Host $_ }
    Write-Host ""
}

# Show latest receipt
$ReceiptPattern = Join-Path $RepoRoot "20_receipts\folder_audit_*.md"
$LatestReceipt = Get-ChildItem $ReceiptPattern -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($LatestReceipt) {
    Write-Host "Receipt: $($LatestReceipt.FullName)"
}

Write-Host ""
Write-Host "Done! Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

exit $ExitCode
