@echo off
setlocal

:: -------------------------------------------------------------------------
:: Batch script to deploy the project from a Git repository.
:: Make sure Git is installed before running this script.
:: To install Git, download the installer from https://git-scm.com/downloads
:: and follow the installation instructions.
:: -------------------------------------------------------------------------

:: User-defined variables
set "REPO_URL=https://github.com/aasem-research-work/aasem-hk.git"
set "PROJECT_DIR=aasem-hk"

:: Check if current directory is the project directory
for /f %%i in ('cd') do set CurrentDir=%%~ni
if "%CurrentDir%"=="%PROJECT_DIR%" (
    echo You are currently in the project directory. Please move deploy.bat outside this directory and try again.
    pause
    goto :EOF
)

:: Check if Git is installed
git --version 2>nul || (
    echo Git is not installed. Please install it from https://git-scm.com/downloads and try again.
    pause
    goto :EOF
)

:: Generate a timestamp
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set "TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%%datetime:~10,2%%datetime:~12,2%"

:: Check if directory exists
if exist "%PROJECT_DIR%" (
    echo Directory %PROJECT_DIR% exists, renaming it...
    rename "%PROJECT_DIR%" "%PROJECT_DIR%-%TIMESTAMP%"
)

echo Cloning GitHub repository...
git clone %REPO_URL%

echo Navigating to project directory...
cd %PROJECT_DIR%

echo Additional setup...
:: Add any additional setup steps here

echo Deployment complete!
endlocal
pause
