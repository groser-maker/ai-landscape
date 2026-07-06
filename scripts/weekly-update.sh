#!/bin/zsh
# AI Landscape — weekly automated update
# Invoked by launchd every Monday at 7:05am (Mac wakes via pmset at 7:00am).
# Runs /ai-landscape --auto-confirm via the Claude CLI.

set -euo pipefail

PROJECT_DIR="/Users/groser/agent-test/claude-projects/AI Landscape/AI Landscape"
LOG_FILE="${PROJECT_DIR}/logs/update.log"
CLAUDE="/Users/groser/.local/bin/claude"

# Rotate log: keep last 500 lines
if [[ -f "$LOG_FILE" ]]; then
  tail -500 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "============================================================" >> "$LOG_FILE"
echo "AI Landscape weekly update — $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "============================================================" >> "$LOG_FILE"

# Source user environment so PATH and any auth tokens are available
source /Users/groser/.zprofile 2>/dev/null || true
source /Users/groser/.zshrc 2>/dev/null || true

cd "$PROJECT_DIR"

"$CLAUDE" --print "/ai-landscape --auto-confirm" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
  echo "✓ Update completed successfully at $(date '+%H:%M:%S')" >> "$LOG_FILE"

  # Stage any changes to data and docs, commit, and push to GitHub Pages
  if ! git diff --quiet || ! git diff --cached --quiet; then
    git add data/ai-landscape.json docs/index.html >> "$LOG_FILE" 2>&1
    git commit -m "AI Landscape auto-update — $(date '+%Y-%m-%d')" >> "$LOG_FILE" 2>&1
    echo "✓ Committed changes" >> "$LOG_FILE"
  else
    echo "— No file changes to commit" >> "$LOG_FILE"
  fi

  git push origin main >> "$LOG_FILE" 2>&1
  PUSH_CODE=$?
  if [[ $PUSH_CODE -eq 0 ]]; then
    echo "✓ Pushed to GitHub — page will update at https://groser-maker.github.io/ai-landscape/" >> "$LOG_FILE"
    # Send Slack DM notification via aisuite MCP proxy
    SLACK_PAYLOAD=$(cat <<'EOJSON'
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"slack_send_message","arguments":{"channel_id":"D01GM8SM4U9","message":"*AI Landscape updated* ✅\n\nThis week's data is live: https://groser-maker.github.io/ai-landscape/"}}}
EOJSON
)
    SLACK_RESP=$(curl -s -X POST "http://127.0.0.1:29051/mcp/servers/slack" \
      -H "Authorization: Bearer cbe13d4f-0eb2-4b41-b7b7-53a2e7061385" \
      -H "Content-Type: application/json" \
      -d "$SLACK_PAYLOAD" 2>&1)
    if echo "$SLACK_RESP" | grep -q "message_link"; then
      echo "✓ Slack DM sent" >> "$LOG_FILE"
    else
      echo "✗ Slack DM failed: $SLACK_RESP" >> "$LOG_FILE"
    fi
  else
    echo "✗ git push FAILED (exit code $PUSH_CODE)" >> "$LOG_FILE"
  fi
else
  echo "✗ Update FAILED (exit code $EXIT_CODE) at $(date '+%H:%M:%S') — skipping push" >> "$LOG_FILE"
fi

exit $EXIT_CODE
