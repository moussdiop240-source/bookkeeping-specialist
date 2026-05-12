@echo off
setlocal EnableDelayedExpansion
title AI Bookkeeping Specialist - Launcher
cd /d "%~dp0"

echo.
echo  ============================================
echo   AI Bookkeeping Specialist  2026 Edition
echo  ============================================
echo.

:: STEP 1: Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found.
    echo.
    echo  Install Python 3.11+ from https://python.org/downloads
    echo  Check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  [OK] Python %PY_VER%

:: STEP 2: Dependencies
echo  [..] Checking Python dependencies...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check >nul 2>&1
echo  [OK] Dependencies ready.

:: STEP 3: Ollama
echo  [..] Checking Ollama AI engine...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] Ollama not found.
    echo  Install Ollama from https://ollama.ai then re-run this launcher.
    echo.
    pause
    exit /b 1
)

curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo  [..] Starting Ollama server...
    start /b ollama serve
    set /a WAIT=0
    :wait_ollama
    timeout /t 1 /nobreak >nul
    curl -s http://localhost:11434 >nul 2>&1
    if not errorlevel 1 goto ollama_ready
    set /a WAIT+=1
    if !WAIT! lss 15 goto wait_ollama
    echo  [WARN] Ollama slow to start. AI features may be unavailable.
    goto model_check
    :ollama_ready
    echo  [OK] Ollama server started.
) else (
    echo  [OK] Ollama server already running.
)

:: STEP 4: Model
:model_check
echo  [..] Checking AI model...
ollama list 2>nul | findstr /i "llama3.2:1b" >nul
if errorlevel 1 (
    echo  [..] Downloading llama3.2:1b model. One-time download, please wait...
    ollama pull llama3.2:1b
    if errorlevel 1 (
        echo  [WARN] Model download failed. AI features may be unavailable.
    ) else (
        echo  [OK] Model ready.
    )
) else (
    echo  [OK] AI model ready.
)

:: STEP 5: Free port 8501 if occupied
echo  [..] Checking port 8501...
netstat -ano | findstr ":8501" | findstr "LISTENING" > "%TEMP%\port8501.txt" 2>nul
for /f "tokens=5" %%p in (%TEMP%\port8501.txt) do (
    taskkill /pid %%p /f >nul 2>&1
)
del "%TEMP%\port8501.txt" >nul 2>&1

:: STEP 6: Launch
echo.
echo  [OK] Starting app. Browser will open in 3 seconds.
echo  Close this window to stop the app.
echo.

start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8501"
python -m streamlit run maker.py --server.headless false --browser.gatherUsageStats false

echo.
echo  App stopped. Press any key to exit.
pause >nul