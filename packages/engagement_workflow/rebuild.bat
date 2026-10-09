@echo off
REM Rebuild EngagementWorkflow.exe
REM Requirements: Python 3.10+ with `pip install pyinstaller requests`

echo Building EngagementWorkflow.exe ...
cd /d "%~dp0"
python -m PyInstaller --clean engagement_workflow.spec

if %ERRORLEVEL% == 0 (
    echo.
    echo SUCCESS: dist\EngagementWorkflow.exe ready.
    echo.
    echo IMPORTANT: Before distributing, do ONE of:
    echo   1. Run: EngagementWorkflow.exe --headless --csv test.csv
    echo      (to refresh the OAuth token next to the .exe)
    echo   2. Or copy .gma_token.json from D:\GR\.gma_token.json
    echo.
    echo DO NOT distribute the test token (dist\.gma_token.json).
    echo.
) else (
    echo FAILED: see errors above.
)
pause
