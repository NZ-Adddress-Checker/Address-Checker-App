@echo off
echo Starting Address Checker App...
docker compose -f docker/docker-compose.yml up -d --build
if %errorlevel% neq 0 (
    echo Failed to start containers. Make sure Docker Desktop is running.
    pause
    exit /b 1
)
echo.
echo App is running at http://localhost:8080
start http://localhost:8080
