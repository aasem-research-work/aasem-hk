@echo off
setlocal enabledelayedexpansion

:: Get the name of the current directory
for %%i in (.) do set current_directory=%%~ni

:: Check if the current directory is aasem-hk
if not "%current_directory%"=="aasem-hk" (
    echo The current directory must be "aasem-hk".
    exit /b
)

:: Set default values
set default_repo=https://github.com/aasem-research-work/aasem-hk
set default_comment=Update

:: Ask for user input
set /p repo=Repo: %default_repo% (Hit Enter, or enter new)
if "!repo!"=="" set repo=%default_repo%

set /p comment=Comments: %default_comment% (Hit Enter, or enter new)
if "!comment!"=="" set comment=%default_comment%

:: Initialize git (if necessary) and add remote (will fail silently if already exists)
git init
git remote add origin %repo% 2> nul

:: Add, commit, and push changes to GitHub
git add .
git commit -m "%comment%"
git push -u origin master

echo Done.

:: Pause the script to see the output (optional)
pause
