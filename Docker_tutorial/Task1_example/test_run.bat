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

:: Set Docker tag and volume name
set "DOCKER_TAG=example-algorithm-task-1-pre-rt-segmentation"
set "DOCKER_NOOP_VOLUME=%DOCKER_TAG%-volume"

:: Set input and output directories
set "INPUT_DIR=%SCRIPT_DIR%\test\input"
set "OUTPUT_DIR=%SCRIPT_DIR%\test\output"

echo =+= Cleaning up any earlier output
if exist "%OUTPUT_DIR%" (
    :: Ensure permissions are setup correctly
    :: This allows for the Docker user to write to this location
    rmdir /s /q "%OUTPUT_DIR%"
    mkdir "%OUTPUT_DIR%"
) else (
    mkdir "%OUTPUT_DIR%"
)

echo =+= (Re)build the container
docker build "%SCRIPT_DIR%" --platform=linux/amd64 --tag %DOCKER_TAG%

echo =+= Doing a forward pass
:: Note: Windows doesn't have a direct equivalent for chmod, so we skip that part

:: Uncomment the next line to enable GPU support
:: set "USE_GPUS=--gpus all"

docker volume create %DOCKER_NOOP_VOLUME%
docker run --rm ^
    --platform=linux/amd64 ^
    --network none ^
    %USE_GPUS% ^
    --volume "%INPUT_DIR%:/input" ^
    --volume "%OUTPUT_DIR%:/output" ^
    --volume "%DOCKER_NOOP_VOLUME%:/tmp" ^
    %DOCKER_TAG%
docker volume rm %DOCKER_NOOP_VOLUME%

:: Windows doesn't have a direct equivalent for chown, so we skip that part

echo =+= Wrote results to %OUTPUT_DIR%

endlocal