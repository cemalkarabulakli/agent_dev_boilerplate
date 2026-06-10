#!/usr/bin/env bash
# setup_morning_reminder_macos.sh
# Registers a launchd agent that generates DASHBOARD.md every morning on macOS.
#
# Usage (run once):
#   bash scripts/setup_morning_reminder_macos.sh
#
# Options:
#   --time HH:MM     Change the daily trigger time (default: 08:00)
#   --email          Include Gmail fetch (--email flag on the script)
#   --remove         Unload and delete the launchd plist

set -euo pipefail

LABEL="dev.agentboilerplate.morning-briefing"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPT="$SCRIPT_DIR/morning_briefing.py"
HOUR=8
MINUTE=0
EMAIL_FLAG=""

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --time)
            IFS=':' read -r HOUR MINUTE <<< "$2"
            HOUR=$((10#$HOUR))
            MINUTE=$((10#$MINUTE))
            shift 2 ;;
        --email)
            EMAIL_FLAG="--email"
            shift ;;
        --remove)
            launchctl unload "$PLIST" 2>/dev/null || true
            rm -f "$PLIST"
            echo "Removed: $PLIST"
            exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

PYTHON="$(command -v python3 || command -v python)"
if [[ -z "$PYTHON" ]]; then
    echo "Error: python3 not found in PATH."
    exit 1
fi

# Build the plist
OPEN_ARG=""
OPEN_PROGRAM_ARG=""
if command -v code &>/dev/null; then
    OPEN_ARG="    <string>--open</string>"
fi

# Build ProgramArguments array
ARGS=("    <string>$PYTHON</string>"
      "    <string>$SCRIPT</string>")
[[ -n "$EMAIL_FLAG" ]] && ARGS+=("    <string>--email</string>")
ARGS+=("    <string>--open</string>")

ARGS_XML=""
for a in "${ARGS[@]}"; do
    ARGS_XML+="      $a"$'\n'
done

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>

  <key>ProgramArguments</key>
  <array>
${ARGS_XML}  </array>

  <key>WorkingDirectory</key>
  <string>${ROOT_DIR}</string>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>${HOUR}</integer>
    <key>Minute</key>
    <integer>${MINUTE}</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>${ROOT_DIR}/logs/morning_briefing.log</string>

  <key>StandardErrorPath</key>
  <string>${ROOT_DIR}/logs/morning_briefing_err.log</string>

  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
EOF

mkdir -p "$ROOT_DIR/logs"

# Load (or reload) the agent
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo ""
echo "launchd agent registered: $LABEL"
echo "  Runs daily at : $(printf '%02d:%02d' "$HOUR" "$MINUTE")"
echo "  Plist file    : $PLIST"
echo "  Working dir   : $ROOT_DIR"
echo "  Email fetch   : ${EMAIL_FLAG:-no (add --email flag to enable)}"
echo ""
echo "Commands:"
echo "  Run now   : launchctl start $LABEL"
echo "  View log  : cat $ROOT_DIR/logs/morning_briefing.log"
echo "  Remove    : bash scripts/setup_morning_reminder_macos.sh --remove"
echo "  Change time: bash scripts/setup_morning_reminder_macos.sh --time 07:00"
