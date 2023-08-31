@echo off
setlocal

:: Navigate to the db directory
cd db

:: Create a new SQLite database named sampledb.db
echo Creating sampledb.db...
sqlite3 sampledb.db ".databases"

:: Execute the DDL and DML SQL scripts
echo Executing DDL.sql...
sqlite3 sampledb.db < DDL.sql

echo Executing DML.sql...
sqlite3 sampledb.db < DML.sql

:: Navigate back to the main directory
cd ..

:: Display a success message
echo Database creation and data insertion complete.

@pause
endlocal
