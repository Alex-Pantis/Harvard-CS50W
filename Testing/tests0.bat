@echo off
python -c "from test0 import test_prime; test_prime(1, False)"
python -c "from test0 import test_prime; test_prime(2, True)"
python -c "from test0 import test_prime; test_prime(8, False)"
python -c "from test0 import test_prime; test_prime(11, True)"
python -c "from test0 import test_prime; test_prime(25, False)"
python -c "from test0 import test_prime; test_prime(28, False)"
echo All tests finished!
pause

REM ==============================================
REM What is this file?
REM This is a "batch file" — a simple script for Windows
REM Name: tests0.bat
REM Purpose: Run 6 quick tests for your is_prime(n) function
REM It works on Windows (cmd or PowerShell) — no Linux or Git Bash needed!
REM ==============================================
