#!/usr/bin/env bash
# ============================================================
#  JMeter Performance Test — headless run with HTML dashboard
#
#  Prerequisites:
#    - Java 17+
#    - Apache JMeter 5.6 on PATH
#      (brew install jmeter  /  apt install jmeter)
#
#  Usage:   ./run_report.sh
# ============================================================

set -euo pipefail
cd "$(dirname "$0")"

# ── Clean previous results ──────────────────────────────────
rm -rf results.jtl dashboard/

echo
echo "============================================================"
echo "  JMeter Performance Test — JSONPlaceholder API"
echo "  Users: 10 | Ramp-up: 5s | Duration: 60s"
echo "============================================================"
echo

# ── Headless run + generate HTML dashboard ──────────────────
jmeter -n \
  -t jsonplaceholder.jmx \
  -l results.jtl \
  -e -o dashboard/ \
  -j jmeter.log

echo
echo "============================================================"
echo "  Dashboard saved to: $(pwd)/dashboard/index.html"
echo "  Open it in a browser to view request statistics,"
echo "  response-time graphs, and throughput charts."
echo "============================================================"
echo
