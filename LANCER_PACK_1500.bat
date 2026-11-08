@echo off
setlocal EnableExtensions
title Pack 1500 - Lancement
cd /d "%~dp0"
chcp 65001 >nul 2>nul
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
set "PORT=8000"

echo.
echo  ==========================================================
echo   PACK 1500 - 1 500 TEMPLATES POWERPOINT PREMIUM
echo   Double-cliquez, attendez, c'est pret.
echo  ==========================================================
echo.

rem --- 1. Trouver Python 3 -------------------------------------------------
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY goto :nopython
%PY% -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" >nul 2>nul
if errorlevel 1 goto :nopython

rem --- 2. Environnement virtuel + dependances ------------------------------
if not exist ".venv\Scripts\python.exe" (
  echo [1/5] Creation de l'environnement Python...
  %PY% -m venv .venv
  if errorlevel 1 goto :erreur
)
set "VENV=%CD%\.venv\Scripts\python.exe"

"%VENV%" -c "import pptx" >nul 2>nul
if errorlevel 1 (
  echo [2/5] Installation de python-pptx (connexion Internet requise)...
  "%VENV%" -m pip install --quiet --disable-pip-version-check -r requirements.txt
  if errorlevel 1 goto :erreur
)

rem --- 3. Catalogue + archive des 1 500 modeles ---------------------------
if not exist "catalog\templates.json" (
  "%VENV%" scripts\export.py --catalogue
  if errorlevel 1 goto :erreur
)

if not exist "dist\Pack-1500-Templates-PowerPoint.zip" (
  echo [3/5] Generation des 1 500 fichiers .pptx - 2 a 3 minutes, patientez...
  "%VENV%" scripts\export.py --all --zip
  if errorlevel 1 goto :erreur
) else (
  echo [3/5] Pack deja present, aucune generation necessaire.
)

rem --- 4. Dezipper les 1 500 fichiers -------------------------------------
echo [4/5] Mise a disposition des 1 500 modeles...
if not exist "dist\Pack-1500-Templates-PowerPoint\INDEX.csv" (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force -LiteralPath '%CD%\dist\Pack-1500-Templates-PowerPoint.zip' -DestinationPath '%CD%\dist'" >nul 2>nul
)

rem --- 5. Galerie web ------------------------------------------------------
echo [5/5] Ouverture de la galerie...
"%VENV%" -c "import urllib.request,json;d=json.load(urllib.request.urlopen('http://127.0.0.1:%PORT%/api/health',timeout=1));assert d['total']==1500" >nul 2>nul
if errorlevel 1 (
  start "Pack 1500 - serveur" /MIN "%VENV%" web\server.py
)
for /L %%i in (1,1,30) do (
  "%VENV%" -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:%PORT%/api/health',timeout=1)" >nul 2>nul && goto :galerie
  timeout /t 1 >nul
)

:galerie
start "" "http://127.0.0.1:%PORT%/"
if exist "%CD%\dist\Pack-1500-Templates-PowerPoint\INDEX.csv" (
  start "" "%CD%\dist\Pack-1500-Templates-PowerPoint"
) else (
  start "" "%CD%\dist"
)

echo.
echo  ==========================================================
echo   C'EST PRET !
echo   - La galerie est ouverte dans votre navigateur
echo   - Le dossier des 1 500 fichiers .pptx est ouvert
echo   - Pour arreter la galerie, fermez la fenetre
echo     minimisee "Pack 1500 - serveur"
echo  ==========================================================
echo.
timeout /t 5 >nul
exit /b 0

:nopython
echo.
echo  PYTHON 3 INTROUVABLE
echo  Installez Python depuis https://www.python.org/downloads/
echo  Cochez bien "Add Python to PATH", puis relancez ce fichier.
echo.
pause
exit /b 1

:erreur
echo.
echo  Une erreur est survenue.
echo  Verifiez la connexion Internet (installation de python-pptx)
echo  puis relancez simplement ce fichier .bat.
echo.
pause
exit /b 1
