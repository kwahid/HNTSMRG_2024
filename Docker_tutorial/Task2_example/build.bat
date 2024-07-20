@echo off
setlocal enabledelayedexpansion

:: Stop at first error
if not defined GOTO (
    set "GOTO=GOTO"
    cmd /c "%~f0" %*
    exit /b !ERRORLEVEL!
)

:: Set script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: Set Docker tag
set "DOCKER_TAG=example-algorithm-task-2-mid-rt-segmentation"

echo =+= Cleaning up any previous builds
:: Remove any existing Docker images with the same tag
for /f %%i in ('docker images -q %DOCKER_TAG%') do (
    echo Removing existing image: %DOCKER_TAG%
    docker rmi %DOCKER_TAG% --force
)

echo =+= Building the Docker image
docker build "%SCRIPT_DIR%" ^
    --platform=linux/amd64 ^
    --tag %DOCKER_TAG%

echo =+= Docker image %DOCKER_TAG% built successfully

endlocal