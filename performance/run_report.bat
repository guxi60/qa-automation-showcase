@echo off
REM ============================================================
REM  Performance test — headless run with HTML report
REM
REM  Usage:   run_report.bat
REM
REM  Parameters (edit below):
REM    -u 10   = 10 concurrent simulated users
REM    -r 2    = spawn 2 users / second
REM    -t 60s  = run for 60 seconds
REM ============================================================

cd /d "%~dp0"

echo.
echo ============================================================
echo   Locust Performance Test — JSONPlaceholder API
echo   Users: 10 | Spawn rate: 2/s | Duration: 60s
echo ============================================================
echo.

locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html report.html

echo.
echo ============================================================
echo   Report saved to: %~dp0report.html
echo   Open it in a browser to view RPS, latency percentiles,
echo   and failure rates.
echo ============================================================
echo.
pause
