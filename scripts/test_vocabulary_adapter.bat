@echo off
REM Quick test script for vocabulary adapter backend (Windows)

echo 🧪 Testing Vocabulary Adapter Backend
echo ======================================
echo.

REM Check if server is running
echo 1. Checking if server is running...
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Server is running
) else (
    echo ❌ Server is not running
    echo    Start it with: python src\servers\main_server.py
    exit /b 1
)

echo.
echo 2. Testing quick endpoint...
curl -s http://localhost:8000/test/vocabulary-adapter/quick

echo.
echo.
echo 3. Testing custom request...
curl -s -X POST http://localhost:8000/test/vocabulary-adapter ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Hello world! SOMA is amazing.\", \"model_name\": \"bert-base-uncased\", \"tokenizer_type\": \"word\"}"

echo.
echo.
echo ✅ Tests complete!
echo.
echo 💡 Tip: Open http://localhost:8000/docs for interactive API testing

pause

