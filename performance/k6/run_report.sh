#!/usr/bin/env bash
# ============================================================
#  K6 Performance Test — headless run with HTML report
#
#  Prerequisites:
#    - Grafana k6 on PATH
#      (brew install k6  /  apt install k6)
#
#  Usage:   ./run_report.sh
# ============================================================

set -euo pipefail
cd "$(dirname "$0")"

# ── Clean previous results ──────────────────────────────────
rm -rf report.html summary.json

echo
echo "============================================================"
echo "  K6 Performance Test — JSONPlaceholder API"
echo "  Scenarios: 5 | Arrival rates: 3/3/2/2/1 per sec"
echo "  Duration: 55 s steady state"
echo "============================================================"
echo

# ── Headless run ────────────────────────────────────────────
k6 run jsonplaceholder.js --summary-export=summary.json

echo
echo "============================================================"
echo "  Report saved to: $(pwd)/report.html"
echo "  Open it in a browser to view request statistics,"
echo "  checks, thresholds, and performance charts."
echo "============================================================"
echo
