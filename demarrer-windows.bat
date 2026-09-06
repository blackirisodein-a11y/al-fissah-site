@echo off
title Al-Fissah - site local
cd /d "%~dp0"
echo.
echo   AL-FISSAH - serveur local
echo   -------------------------
echo   Le site s'ouvre dans votre navigateur.
echo   Laissez cette fenetre ouverte pendant que vous consultez le site.
echo   Pour arreter : fermez cette fenetre.
echo.
start "" http://localhost:8000
python -m http.server 8000 2>nul || py -m http.server 8000
pause
