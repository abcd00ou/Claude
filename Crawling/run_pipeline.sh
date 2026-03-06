#!/bin/bash
# Price Intelligence Pipeline — cron 실행 스크립트

export PATH="/opt/homebrew/opt/postgresql@17/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/cron.log"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

echo "========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 파이프라인 시작" >> "$LOG_FILE"

cd "$SCRIPT_DIR" && \
  "$PYTHON" run_pipeline.py --country US JP DE >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 종료 (exit=$EXIT_CODE)" >> "$LOG_FILE"
