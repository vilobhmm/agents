#!/bin/bash
# Debug script to capture conversation history logs
# Run this on your Mac to see what's being sent to Claude API

set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source agents-venv/bin/activate

# Create queue directory if it doesn't exist
echo "📁 Creating queue directory..."
mkdir -p ~/.agency/queue/chats/cc_team

echo "🔍 Clearing queue..."
rm -f ~/.agency/queue/chats/cc_team/*.md

echo "📝 Creating test message..."
cat > ~/.agency/queue/chats/cc_team/test_$(date +%Y-%m-%dT%H:%M:%S).md << 'EOF'
# Team Conversation: CC Productivity Team
**Date:** 2026-02-17T10:00:00
**Channel:** telegram | **Sender:** vm_test
**Messages:** 1

## User Message
@cc What's on my calendar today?
EOF

# Clear old processor log
rm -f logs/processor.log

echo "🚀 Starting message processor (will run for 10 seconds)..."
echo "📊 Watch for these log lines:"
echo "  - '🔍 Conversation history length: X messages'"
echo "  - '🔍 History[N]: role - content...'"
echo ""

# Start processor for 10 seconds
timeout 10 python -m agency.processor 2>&1 | tee /tmp/agency_conversation_debug.log || true

# Also check the processor.log file if it exists
if [ -f "logs/processor.log" ]; then
    echo ""
    echo "📋 Processor log contents:"
    cat logs/processor.log >> /tmp/agency_conversation_debug.log
fi

echo ""
echo "📋 Extracting conversation history logs..."
grep -A 10 "Conversation history" /tmp/agency_conversation_debug.log || echo "❌ No conversation history logs found"

echo ""
echo "📋 Extracting Claude API calls..."
grep -B 5 -A 5 "Sending.*tools to Claude API" /tmp/agency_conversation_debug.log || echo "❌ No tool logs found"

echo ""
echo "📋 Checking for the '18' response..."
grep -B 10 -A 10 "^\s*18\s*$" /tmp/agency_conversation_debug.log || echo "✅ No '18' response found in logs"

echo ""
echo "📄 Full log saved to: /tmp/agency_conversation_debug.log"
echo "📄 You can review it with: cat /tmp/agency_conversation_debug.log"
