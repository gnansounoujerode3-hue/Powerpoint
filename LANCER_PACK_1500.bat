@echo off
rem ============================================================
rem  PACK 1500 - lanceur Windows
rem  Version "flat" : AUCUN bloc entre parentheses, uniquement
rem  des chemins relatifs. Indispensable quand le dossier du
rem  projet contient des parentheses, ex. Powerpoint 1.
rem ============================================================
if "%~1"==":run" goto :debut
start "Pack 1500" cmd /k "%~f0" :run
exit /b

:debut
setlocal EnableExtensions
title Pack 1500 - Lancement
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PORT=8000"
set "LOG=LANCER_PACK_1500.log"
set "VENV=%CD%\.venv\Scripts\python.exe"
set "OUTDIR=%CD%\dist\Pack-1500-Templates-PowerPoint"

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
if defined PY goto :pytest
where python >nul 2>nul && set "PY=python"
:pytest
if not defined PY goto :nopython
%PY% -c "import sys" >nul 2>nul
if errorlevel 1 goto :nopython
%PY% -c "import sys;sys.exit(3-sys.version_info[0])" >nul 2>nul
if errorlevel 1 goto :nopython
echo [1/5] Python 3 detecte : %PY% >> "%LOG%"
echo [1/5] Python 3 detecte.

rem --- 2. Environnement virtuel + dependances -------------------
if exist ".venv\Scripts\python.exe" goto :venvok
echo [2/5] Creation de l'environnement Python...
echo [2/5] venv >> "%LOG%"
%PY% -m venv .venv >> "%LOG%" 2>&1
if errorlevel 1 goto :erreur
:venvok
if not exist "%VENV%" goto :erreur

"%VENV%" -c "import pptx" >nul 2>nul
if not errorlevel 1 goto :pipok
echo [2/5] Installation de python-pptx - Internet requis...
echo [2/5] pip install >> "%LOG%"
"%VENV%" -m pip install --quiet --disable-pip-version-check -r requirements.txt >> "%LOG%" 2>&1
if errorlevel 1 goto :erreur
"%VENV%" -c "import pptx" >nul 2>nul
if errorlevel 1 goto :erreur
:pipok
echo [2/5] Dependances OK >> "%LOG%"

rem --- 3. Catalogue + archive des 1 500 modeles ----------------
if exist "catalog\templates.json" goto :catok
echo [3/5] Creation du catalogue...
"%VENV%" scripts\export.py --catalogue >> "%LOG%" 2>&1
if errorlevel 1 goto :erreur
:catok
if exist "dist\Pack-1500-Templates-PowerPoint.zip" goto :zipok
echo [3/5] Generation des 1 500 fichiers .pptx...
echo        Patientez 2 a 3 minutes, c'est normal.
echo [3/5] export --all --zip >> "%LOG%"
"%VENV%" scripts\export.py --all --zip >> "%LOG%" 2>&1
if errorlevel 1 goto :erreur
:zipok
echo [3/5] Archive OK >> "%LOG%"

rem --- 4. Dezipper les 1 500 fichiers --------------------------
echo [4/5] Preparation du dossier des 1 500 .pptx...
if exist "dist\Pack-1500-Templates-PowerPoint\INDEX.csv" goto :unzipok
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force -LiteralPath 'dist\Pack-1500-Templates-PowerPoint.zip' -DestinationPath 'dist'" >> "%LOG%" 2>&1
:unzipok
echo [4/5] Extraction OK >> "%LOG%"

rem --- 5. Galerie web -------------------------------------------
echo [5/5] Ouverture de la galerie...
"%VENV%" -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=1)" >nul 2>nul
if not errorlevel 1 goto :servok
start "Pack 1500 - serveur" /MIN "%VENV%" web\server.py
timeout /t 5 >nul
:servok
start "" "http://127.0.0.1:8000/"
if exist "dist\Pack-1500-Templates-PowerPoint\INDEX.csv" goto :outdossier
start "" "dist"
goto :ouvfait
:outdossier
start "" "%OUTDIR%"
:ouvfait
echo [5/5] Termine >> "%LOG%"

echo.
echo  ==========================================================
echo   C'EST PRET !
echo   - Galerie : http://127.0.0.1:8000/
echo   - 1 500 .pptx : dossier dist ouvert
echo   - Journal : %LOG%
echo   - Pour arreter le serveur : fermez la fenetre
echo     minimisee "Pack 1500 - serveur"
echo  ==========================================================
echo.
echo Vous pouvez fermer cette fenetre quand vous voulez.
exit /b 0

:dossier
echo.
echo  ERREUR : CE FICHIER .BAT EST TOUT SEUL.
echo  Il doit etre a la racine du projet, a cote de :
echo  core\   scripts\   web\   requirements.txt
echo.
echo  Dossier actuel : %CD%
echo  Journal : %LOG%
echo.
pause
exit /b 1

:nopython
echo.
echo  ERREUR : PYTHON 3 INTROUVABLE.
echo  Installez Python 3 depuis https://www.python.org/downloads/
echo  Cochez bien "Add Python to PATH", puis relancez ce .bat.
echo.
echo  Journal : %LOG%
echo.
pause
exit /b 1

:erreur
echo.
echo  ERREUR : une etape a echoue.
echo  Consultez le journal : %LOG%
echo  Ouvrez le fichier .log avec le Bloc-notes
echo.
echo  Causes frequentes : pas d'Internet pour pip,
echo  espace disque insuffisant, ou antivirus qui bloque.
echo.
pause
exit /b 1
