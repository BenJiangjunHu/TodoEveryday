@echo off
echo Building TodoEveryday Spring Boot Backend...

REM Clean and build the project
call mvn clean install

if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully!
    echo You can now run the application with: mvn spring-boot:run
    echo Or run: java -jar target/todo-backend-1.0.0.jar
) else (
    echo Build failed!
    exit /b 1
)

pause
