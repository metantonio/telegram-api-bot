echo Ubicacion Carpeta
cd /d %~dp0
@echo off
echo:
@echo on
pipenv shell
echo pipenv run main2.py
PAUSE