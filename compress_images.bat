@echo off
REM Image Compression Script for Windows
REM This script compresses all images in your portfolio folders

echo.
echo ============================================
echo  Sylva Lens - Image Compression Tool
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please download Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if Pillow is installed
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required package (Pillow)...
    echo.
    pip install Pillow
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow
        pause
        exit /b 1
    )
)

REM Run the compression script
echo Starting image compression process...
echo.
python compress_images.py
echo.
echo Press any key to exit...
pause
