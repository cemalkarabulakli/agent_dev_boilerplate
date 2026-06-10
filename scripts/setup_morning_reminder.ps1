# setup_morning_reminder.ps1
# Registers a Windows Task Scheduler task that generates DASHBOARD.md every morning.
#
# Usage (run once, no admin required for current-user tasks):
#   PowerShell -ExecutionPolicy Bypass -File scripts/setup_morning_reminder.ps1
#
# Options:
#   -Time "07:30"    Change the daily trigger time (default: 08:00)
#   -Remove          Unregister the task and exit
#   -Email           Include Gmail fetch (--email flag on the script)
#
# After setup, to run immediately:
#   Start-ScheduledTask -TaskName "AgentBoilerplate_MorningBriefing"

param(
    [string] $Time   = "08:00",
    [switch] $Remove,
    [switch] $Email
)

$TaskName  = "AgentBoilerplate_MorningBriefing"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir   = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$Script    = Join-Path $ScriptDir "morning_briefing.py"

if ($Remove) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Task '$TaskName' removed."
    exit 0
}

$Python = (Get-Command python -ErrorAction SilentlyContinue)?.Source
if (-not $Python) {
    Write-Error "python not found in PATH. Install Python 3.11+ and retry."
    exit 1
}

$EmailFlag = if ($Email) { " --email" } else { "" }
$Arguments = "`"$Script`"$EmailFlag --open"

$Action   = New-ScheduledTaskAction -Execute $Python -Argument $Arguments -WorkingDirectory $RootDir
$Trigger  = New-ScheduledTaskTrigger -Daily -At $Time
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 3) `
    -StartWhenAvailable `
    -WakeToRun

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action   $Action `
    -Trigger  $Trigger `
    -Settings $Settings `
    -RunLevel Limited `
    -Force | Out-Null

Write-Host ""
Write-Host "Task registered: $TaskName"
Write-Host "  Runs daily at : $Time"
Write-Host "  Script        : $Script"
Write-Host "  Working dir   : $RootDir"
Write-Host "  Email fetch   : $(if ($Email) { 'yes (--email)' } else { 'no (add -Email flag to enable)' })"
Write-Host ""
Write-Host "Commands:"
Write-Host "  Run now   : Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "  Remove    : PowerShell -File scripts/setup_morning_reminder.ps1 -Remove"
Write-Host "  Change time: PowerShell -File scripts/setup_morning_reminder.ps1 -Time '07:00'"
