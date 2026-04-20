@echo off
echo Optimizing images for Sylva Lens website...
echo.

cd /d "%~dp0"

REM Check if ImageMagick is installed
magick -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ImageMagick is not installed. Please install it from: https://imagemagick.org/
    echo Or use online tools like TinyPNG, Squoosh, or ImageOptim.
    pause
    exit /b 1
)

echo Creating optimized versions...
echo.

REM Create optimized JPEG versions (80% quality, progressive)
for %%f in (Weddings\*.jpg Weddings\*.jpeg Weddings\*.JPG) do (
    echo Optimizing %%f
    magick "%%f" -quality 80 -interlace JPEG -strip "optimized\%%~nf.jpg"
)

REM Create WebP versions (75% quality for better compression)
for %%f in (Weddings\*.jpg Weddings\*.jpeg Weddings\*.JPG) do (
    echo Creating WebP for %%f
    magick "%%f" -quality 75 -define webp:lossless=false "optimized\%%~nf.webp"
)

echo.
echo Optimization complete! Check the 'optimized' folder.
echo.
echo Summary of optimizations:
echo - JPEG quality reduced to 80%% with progressive loading
echo - WebP versions created with 75%% quality
echo - Metadata stripped to reduce file size
echo.
pause