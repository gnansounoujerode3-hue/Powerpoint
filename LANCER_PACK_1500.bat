@echo off
rem ============================================================
rem  PACK 1500 - lanceur Windows
rem  Auto-relaunch dans cmd /k : la fenetre ne se ferme jamais.
rem ============================================================
if not "%~1"==":run" (
  start "Pack 1500" cmd /k "%~f0" :run
  exit /b
)
setlocal EnableExtensions
title Pack 1500 - Lancement
cd /d "%~dp0"

set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PORT=8000"
set "LOG=%CD%\LANCER_PACK_1500.log"

echo === PACK 1500 - JOURNAL %DATE% %TIME% === > "%LOG%"
echo Dossier : %CD% >> "%LOG%"

echo.
echo  ==========================================================
echo   PACK 1500 - 1 500 TEMPLATES POWERPOINT
echo   Lancement automatique. Laissez cette fenetre ouverte.
echo  ==========================================================
echo.

rem --- 0. Le .bat doit etre dans le dossier du projet ----------
if not exist "scripts\export.py" goto :dossier
if not exist "core\design_system.py" goto :dossier
if not exist "requirements.txt" goto :dossier
echo [0/5] Dossier du projet OK >> "%LOG%"

rem --- 1. Trouver Python 3 --------------------------------------
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY goto :nopython
%PY% -c "import sys" >nul 2>nul
if errorlevel 1 goto :nopython
%PY% -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" >nul 2>nul
if errorlevel 1 goto :nopython
echo [1/5] Python 3 detecte : %PY% >> "%LOG%"
echo [1/5] Python 3 detecte.

rem --- 2. Environnement virtuel + dependances -------------------
if not exist ".venv\Scripts\python.exe" (
  echo [2/5] Creation de l'environnement Python...
  echo [2/5] venv >> "%LOG%"
  %PY% -m venv .venv >> "%LOG%" 2>&1
  if errorlevel 1 goto :erreur
)
set "VENV=%CD%\.venv\Scripts\python.exe"
if not exist "%VENV%" goto :erreur

"%VENV%" -c "import pptx" >nul 2>nul
if errorlevel 1 (
  echo [2/5] Installation de python-pptx (Internet requis)...
  echo [2/5] pip install >> "%LOG%"
  "%VENV%" -m pip install --quiet --disable-pip-version-check -r requirements.txt >> "%LOG%" 2>&1
  if errorlevel 1 goto :erreur
)
"%VENV%" -c "import pptx" >nul 2>nul
if errorlevel 1 goto :erreur
echo [2/5] Dependances OK >> "%LOG%"

rem --- 3. Catalogue + archive des 1 500 modeles ----------------
if not exist "catalog\templates.json" (
  echo [3/5] Creation du catalogue...
  "%VENV%" scripts\export.py --catalogue >> "%LOG%" 2>&1
  if errorlevel 1 goto :erreur
)
if not exist "dist\Pack-1500-Templates-PowerPoint.zip" (
  echo [3/5] Generation des 1 500 fichiers .pptx...
  echo        Patientez 2 a 3 minutes, c'est normal.
  echo [3/5] export --all --zip >> "%LOG%"
  "%VENV%" scripts\export.py --all --zip >> "%LOG%" 2>&1
  if errorlevel 1 goto :erreur
) else (
  echo [3/5] Pack deja present, rien a regenerer.
)
echo [3/5] Archive OK >> "%LOG%"

rem --- 4. Dezipper les 1 500 fichiers --------------------------
echo [4/5] Preparation du dossier des 1 500 .pptx...
if not exist "dist\Pack-1500-Templates-PowerPoint\INDEX.csv" (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force -LiteralPath '%CD%\dist\Pack-1500-Templates-PowerPoint.zip' -DestinationPath '%CD%\dist'" >> "%LOG%" 2>&1
)
echo [4/5] Extraction OK >> "%LOG%"

rem --- 5. Galerie web -------------------------------------------
echo [5/5] Ouverture de la galerie...
"%VENV%" -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=1)" >nul 2>nul
if errorlevel 1 (
  start "Pack 1500 - serveur" /MIN "%VENV%" web\server.py
  timeout /t 5 >nul
)
start "" "http://127.0.0.1:8000/"
if exist "%CD%\dist\Pack-1500-Templates-PowerPoint\INDEX.csv" (
  start "" "%CD%\dist\Pack-1500-Templates-PowerPoint"
) else (
  start "" "%CD%\dist"
)
echo [5/5] Termine >> "%LOG%"

echo.
echo  ==========================================================
echo   C'EST PRET !
echo   - Galerie : http://127.0.0.1:8000/
echo   - 1 500 .pptx : dossier dist ouvert
echo   - Journal : LANCER_PACK_1500.log
echo   - Pour arreter le serveur : fermez la fenetre
echo     minimisee "Pack 1500 - serveur"
echo  ==========================================================
echo.
echo Vous pouvez fermer cette fenetre quand vous voulez.
exit /b 0

:dossier
echo.
echo  ERREUR : CE FICHIER .BAT EST TOUT SEUL.
echo.
echo  Il doit etre place A LA RACINE du dossier du projet,
echo  a cote de : core\  scripts\  web\  requirements.txt
echo.
echo  Telechargez tout le projet (ou clonez le depot GitHub),
echo  copiez LANCER_PACK_1500.bat dedans, puis double-cliquez.
echo.
echo  Dossier actuel : %CD%
echo.
pause
exit /b 1

:nopython
echo.
echo  ERREUR : PYTHON 3 INTROUVABLE.
echo.
echo  Installez Python 3 depuis https://www.python.org/downloads/
echo  Cochez bien "Add Python to PATH" pendant l'installation,
echo  puis relancez ce fichier .bat.
echo.
echo  Journal : "%LOG%"
echo.
pause
exit /b 1

:erreur
echo.
echo  ERREUR : une etape a echoue.
echo.
echo  Consultez le journal pour le detail :
echo    "%LOG%"
echo.
echo  Causes frequentes : pas d'Internet pour pip,
echo  espace disque insuffisant, ou antivirus qui bloque.
echo  Relancez simplement ce .bat apres correction.
echo.
pause
exit /b 1
