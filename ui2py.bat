@echo off
setlocal EnableDelayedExpansion

:: -------------------------------------------------------------------------
:: Batch script to convert .ui files to .py files and res_main.qrc to res_main_rc.py
:: -------------------------------------------------------------------------

:: Loop through all .ui files in the current directory
for %%F in (*.ui) do (
    :: Extract the filename without the extension
    set "filename=%%~nF"
    
    :: Convert .ui to .py using pyuic5
    pyuic5 -x "%%F" -o "!filename!.py"
    echo Converted %%F to !filename!.py
)

:: Convert res_main.qrc to res_main_rc.py
pyrcc5 res_main.qrc -o res_main_rc.py
echo res_main.qrc converted to res_main_rc.py

:: End the script
echo Conversion complete.
endlocal
