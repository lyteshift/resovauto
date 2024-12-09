@echo off
IF EXIST praise_the_omnissiah.md GOTO :pyvenvinstalled
ECHO Strike the first rune upon the engine's casing employing the chosen wrench. Its tip should be anointed with the oil of engineering using the proper incantation when the auspices are correct. Strike the second rune upon the engine's casing employing the arc-tip of the power-driver. If the second rune is not good, a third rune may be struck in like manner to the first. This is done according to the true ritual laid down by Scotti the Enginseer. A libation should be offered. If this sequence is properly observed the engines may be brought to full activation by depressing the large panel marked ON. > praise_the_omnissiah.md

winget list | findstr Python >nul

IF %ERRORLEVEL% EQU 0 GOTO :pyinstalled
@echo on
echo Installing Python...
winget install python
@echo off

:pyinstalled
IF EXIST .venv .venv\Scripts\activate GOTO :venvinstalled
@echo on
echo Activating VENV...
python -m venv .venv
@echo off

:venvinstalled
@echo on
.\.venv\Scripts\pip install -r requirements.txt
@echo off

:pyvenvinstalled
.\.venv\Scripts\python main.py
