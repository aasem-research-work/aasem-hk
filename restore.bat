@echo off
setlocal

:: -------------------------------------------------------------------------
:: Batch script to restore the 'db' directory.
:: -------------------------------------------------------------------------

:: User-defined variables
set "SOURCE_DIR=..\backup\db"
set "DEST_DIR=db"

:: Generate a timestamp
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set "TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%%datetime:~10,2%%datetime:~12,2%"

:: Check if 'db' directory exists in the backup directory
if not exist "%SOURCE_DIR%" (
    echo Source directory "%SOURCE_DIR%" does not exist. Exiting...
    goto :EOF
)

:: Check if 'db' directory already exists in the current directory
if exist "%DEST_DIR%" (
    echo Directory %DEST_DIR% already exists in the current directory, renaming it...
    rename "%DEST_DIR%" "%DEST_DIR%-%TIMESTAMP%"
)

:: Perform the restore
echo Restoring "%SOURCE_DIR%" to "%DEST_DIR%"...
xcopy /s /i "%SOURCE_DIR%" "%DEST_DIR%"

echo Restore complete!
endlocal
pause
