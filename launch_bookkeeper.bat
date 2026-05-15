@echo off
setlocal EnableDelayedExpansion
title AI Bookkeeping Specialist - Starting...
cd /d "%~dp0"

cls
echo.
echo  +========================================================+
echo  ^|      AI Bookkeeping Specialist  2026 Edition          ^|
echo  ^|         IRS ^& GAAP Compliant  -  100%% Local AI       ^|
echo  +========================================================+
echo.

:: --- BONUS: Desktop shortcut with professional icon (first run) ---
if not exist "%USERPROFILE%\Desktop\AI Bookkeeper.lnk" (
    echo  [..] Creating desktop shortcut with custom icon...
    set "BATCH_PATH=%~f0"
    set "WORK_DIR=%~dp0"
    (
        echo Set ws = CreateObject^("WScript.Shell"^)
        echo Set sc = ws.CreateShortcut^(ws.ExpandEnvironmentStrings^("%%USERPROFILE%%\Desktop\AI Bookkeeper.lnk"^)^)
        echo sc.TargetPath     = "!BATCH_PATH!"
        echo sc.WorkingDirectory = "!WORK_DIR!"
        echo sc.IconLocation   = "%SystemRoot%\System32\shell32.dll, 13"
        echo sc.Description    = "AI Bookkeeping Specialist 2026"
        echo sc.WindowStyle    = 1
        echo sc.Save
    ) > "%TEMP%\mkshortcut.vbs"
    cscript //nologo "%TEMP%\mkshortcut.vbs" >nul 2>&1
    del "%TEMP%\mkshortcut.vbs" >nul 2>&1
    echo  [OK] Shortcut added to Desktop: "AI Bookkeeper"
    echo.
)

:: --- STEP 1: Python environment ---
echo  [1/4] Python environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo  [OK] Virtual environment activated ^(venv^).
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo  [OK] Virtual environment activated ^(.venv^).
) else if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
    echo  [OK] Virtual environment activated ^(env^).
) else (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo  [ERROR] Python not found. Install Python 3.11+ from https://python.org
        echo          Enable "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    )
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
    echo  [OK] System Python !PY_VER!
)

:: --- STEP 2: Dependencies ---
echo  [2/4] Verifying dependencies...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check >nul 2>&1
echo  [OK] All packages ready.

:: --- STEP 3: Ollama - check, then start if needed ---
echo  [3/4] Ollama AI engine...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] Ollama not found. Install from https://ollama.ai then re-run.
    echo.
    pause
    exit /b 1
)

curl -s --max-time 2 http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo  [..] Ollama is not running - starting server...
    start /b ollama serve
    set /a WAIT=0
    :wait_ollama
    timeout /t 1 /nobreak >nul
    curl -s --max-time 2 http://localhost:11434 >nul 2>&1
    if not errorlevel 1 goto ollama_ready
    set /a WAIT+=1
    if !WAIT! lss 15 goto wait_ollama
    echo  [WARN] Ollama is slow to respond. AI features may be limited.
    goto launch_app
    :ollama_ready
    echo  [OK] Ollama server started (took !WAIT!s).
) else (
    echo  [OK] Ollama server already running.
)

:: --- STEP 4: Clear port 8501, then launch ---
:launch_app
echo  [4/4] Launching application...
netstat -ano | findstr ":8501" | findstr "LISTENING" > "%TEMP%\port8501.txt" 2>nul
for /f "tokens=5" %%p in (%TEMP%\port8501.txt) do (
    taskkill /pid %%p /f >nul 2>&1
)
del "%TEMP%\port8501.txt" >nul 2>&1

echo.
echo  +--------------------------------------------------+
echo  ^|  Browser will open automatically in ~3 seconds.  ^|
echo  ^|  Close this window to stop the application.      ^|
echo  +--------------------------------------------------+
echo.

title AI Bookkeeping Specialist - Running on http://localhost:8501
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8501"
python -m streamlit run maker.py --server.headless false --browser.gatherUsageStats false

echo.
echo  Application stopped.  Press any key to exit.
pause >nul
