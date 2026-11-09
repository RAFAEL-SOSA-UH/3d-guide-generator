@echo off
chcp 65001 >nul
REM Creates a .venv virtual environment for this tool only and installs its dependencies.
REM Double-click once. To reinstall from scratch, delete the .venv folder and run it again.

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python not found. Install it from https://www.python.org/downloads/
  echo and tick "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo Could not create the virtual environment.
    pause
    exit /b 1
  )
)

echo Installing dependencies into .venv ...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo.
where ffmpeg >nul 2>nul
if errorlevel 1 (
  echo WARNING: ffmpeg not found. Install it with:  winget install Gyan.FFmpeg
  echo then close and reopen this window.
) else (
  echo ffmpeg: found.
)
where tesseract >nul 2>nul
if errorlevel 1 (
  echo Optional: to read on-screen text install Tesseract:  winget install UB-Mannheim.TesseractOCR
) else (
  echo tesseract: found. OCR will be used.
)

echo.
echo Ready. Drag a video onto process.bat
pause
