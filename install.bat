@echo off
echo ================================================
echo   SV Recharge - Mantra Bridge Installer
echo ================================================
echo.

echo Installing Mantra Bridge...
mkdir "%PROGRAMFILES%\SVRecharge" 2>nul
copy MantraBridge.exe "%PROGRAMFILES%\SVRecharge\" >nul

echo Adding to Windows startup...
set STARTUP="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTUP%\MantraBridge.lnk');$s.TargetPath='%PROGRAMFILES%\SVRecharge\MantraBridge.exe';$s.Save()"

echo Creating desktop shortcut...
set DESKTOP="%USERPROFILE%\Desktop"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\Mantra Bridge.lnk');$s.TargetPath='%PROGRAMFILES%\SVRecharge\MantraBridge.exe';$s.Save()"

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo Starting Mantra Bridge now...
start "" "%PROGRAMFILES%\SVRecharge\MantraBridge.exe"
echo.
echo You can now use svrecharge.in with your device!
echo.
pause