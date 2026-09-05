@echo off

for /f "usebackq delims=" %%T in (`powershell.exe -NoProfile -Command "$s = Read-Host 'Paste the repository-scoped agent PAT' -AsSecureString; [Console]::Out.Write([System.Net.NetworkCredential]::new('', $s).Password)"`) do set "GH_TOKEN=%%T"

if not defined GH_TOKEN (
    echo ERROR: No token was captured.
    exit /b 1
)

set "PIP_REQUIRE_VIRTUALENV=true"
echo Restricted GitHub credential loaded for this Command Prompt session.
echo PIP_REQUIRE_VIRTUALENV is enabled.
exit /b 0

