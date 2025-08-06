@echo off
echo Starting TodoEveryday Spring Boot Backend...

REM Start the Spring Boot application
call mvn spring-boot:run

if %ERRORLEVEL% NEQ 0 (
    echo Failed to start the application!
    echo Make sure you have built the project first with: build.bat
    pause
    exit /b 1
)
