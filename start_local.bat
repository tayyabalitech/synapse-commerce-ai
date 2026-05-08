@echo off
title SynapseCommerce AI - Local Server
echo.
echo ========================================================
echo    SynapseCommerce AI - Localhost Deployment
echo ========================================================
echo.

:: Start Backend (FastAPI on port 8000)
echo [1/2] Starting Backend (FastAPI) on http://localhost:8000 ...
start "SynapseCommerce Backend" cmd /k "cd /d %~dp0 && call venv\Scripts\activate && uvicorn backend.main:app --reload --port 8000"

:: Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak > nul

:: Start Frontend (Next.js on port 3000)
echo [2/2] Starting Frontend (Next.js) on http://localhost:3000 ...
start "SynapseCommerce Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================================
echo    ALL SYSTEMS ONLINE
echo ========================================================
echo.
echo    Backend:    http://localhost:8000
echo    Frontend:   http://localhost:3000
echo    Trigger AI: http://localhost:8000/run-discovery
echo    API Docs:   http://localhost:8000/docs
echo.
echo    Press any key to close this launcher window...
echo    (The servers will keep running in their own windows)
echo ========================================================
pause > nul
