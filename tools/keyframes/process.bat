@echo off
chcp 65001 >nul
REM Drag a video onto this file.
REM If a .srt, .vtt, .txt or .md with the same name sits next to the video, it is used as the transcript.
REM The result goes to output\<video name>\

set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo The .venv environment does not exist. Run install.bat first.
  pause
  exit /b 1
)

if "%~1"=="" (
  echo Drag a video file onto process.bat
  pause
  exit /b 1
)

set "VIDEO=%~1"
set "BASE=%~dpn1"
set "TRANS="
if exist "%BASE%.srt" set "TRANS=%BASE%.srt"
if exist "%BASE%.vtt" set "TRANS=%BASE%.vtt"
if exist "%BASE%.txt" set "TRANS=%BASE%.txt"
if exist "%BASE%.md"  set "TRANS=%BASE%.md"

set "OCR="
where tesseract >nul 2>nul && set "OCR=--ocr"

if defined TRANS (
  echo Transcript: %TRANS%
  "%PY%" "%~dp0keyframes.py" "%VIDEO%" -t "%TRANS%" %OCR%
) else (
  echo No transcript: no .srt, .vtt, .txt or .md with the same name as the video
  "%PY%" "%~dp0keyframes.py" "%VIDEO%" %OCR%
)
pause
