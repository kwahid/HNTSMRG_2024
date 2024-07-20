@echo off
setlocal enabledelayedexpansion

:: Stop at first error
if not defined GOTO (
    set "GOTO=GOTO"
    cmd /c "%~f0" %*
    exit /b !ERRORLEVEL!
)

:: Run the build script
call build.bat

:: Set Docker tag
set "DOCKER_TAG=example-algorithm-task-2-mid-rt-segmentation"

echo =+= Exporting the Docker image to a tar.gz file
docker save %DOCKER_TAG% > %DOCKER_TAG%.tar

:: Use PowerShell to gzip the tar file
powershell -command "& { $input = [System.IO.File]::OpenRead('%DOCKER_TAG%.tar'); $output = [System.IO.File]::Create('%DOCKER_TAG%.tar.gz'); $gzipStream = New-Object System.IO.Compression.GzipStream $output, ([IO.Compression.CompressionMode]::Compress); $input.CopyTo($gzipStream); $gzipStream.Close(); $output.Close(); $input.Close(); }"

:: Clean up the temporary tar file
del %DOCKER_TAG%.tar

echo =+= Docker image exported successfully to %DOCKER_TAG%.tar.gz

endlocal