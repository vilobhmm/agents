#!/bin/bash
# Debug script to capture conversation history logs
# Run this on your Mac to see what's being sent to Claude API

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

echo "🚀 Starting agency system (will run for 30 seconds)..."
echo "📊 Watch for these log lines:"
echo "  - '🔍 Conversation history length: X messages'"
echo "  - '🔍 History[N]: role - content...'"
echo ""

cd ~/agents
timeout 30 python -m agency start 2>&1 | tee /tmp/agency_conversation_debug.log

echo ""
echo "📋 Extracting conversation history logs..."
grep -A 10 "Conversation history" /tmp/agency_conversation_debug.log || echo "❌ No conversation history logs found"

echo ""
echo "📋 Extracting Claude API calls..."
grep -B 5 -A 5 "Sending.*tools to Claude API" /tmp/agency_conversation_debug.log || echo "❌ No tool logs found"

echo ""
echo "📄 Full log saved to: /tmp/agency_conversation_debug.log"
echo "📄 You can review it with: cat /tmp/agency_conversation_debug.log"
