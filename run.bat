@echo off
setlocal

:: -------------------------------------------------------------------------
:: Batch script to activate the pyqt5 environment and run main.py
:: -------------------------------------------------------------------------

:: Activate the pyqt5 environment
call activate pyqt5

:: Run main.py
python main.py

:: End the script
endlocal
pause
