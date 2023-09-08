@echo off
setlocal

:: -------------------------------------------------------------------------
:: Batch script to backup the 'db' directory.
:: -------------------------------------------------------------------------

:: User-defined variables
set "SOURCE_DIR=db"
set "BACKUP_DIR=..\backup"

:: Generate a timestamp
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set "TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%%datetime:~10,2%%datetime:~12,2%"

:: Check if 'db' directory exists in the current directory
if not exist "%SOURCE_DIR%" (
    echo Source directory "%SOURCE_DIR%" does not exist. Exiting...
    goto :EOF
)

:: Check and create the backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" (
    echo Creating backup directory...
    mkdir "%BACKUP_DIR%"
)

:: Check if 'db' directory already exists in the backup directory
if exist "%BACKUP_DIR%\%SOURCE_DIR%" (
    echo Directory %SOURCE_DIR% already exists in the backup directory, renaming it...
    rename "%BACKUP_DIR%\%SOURCE_DIR%" "%SOURCE_DIR%-%TIMESTAMP%"
)

:: Perform the backup
echo Backing up "%SOURCE_DIR%" to "%BACKUP_DIR%"...
xcopy /s /i "%SOURCE_DIR%" "%BACKUP_DIR%\%SOURCE_DIR%"

echo Backup complete!
endlocal
pause
