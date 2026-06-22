#!/usr/bin/env bash
# ============================================================
#  Performance test — headless run with HTML report
#
#  Usage:   ./run_report.sh
# ============================================================

set -euo pipefail
cd "$(dirname "$0")"

echo
echo "============================================================"
echo "  Locust Performance Test — JSONPlaceholder API"
echo "  Users: 10 | Spawn rate: 2/s | Duration: 60s"
echo "============================================================"
echo

locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html report.html

echo
echo "============================================================"
echo "  Report saved to: $(pwd)/report.html"
echo "============================================================"
echo
