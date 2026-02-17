#!/bin/bash
# Simple test - check where CC's response went

echo "📋 Checking outgoing queue..."
ls -la ~/.agency/queue/outgoing/
if [ -f ~/.agency/queue/outgoing/*.json ]; then
    echo ""
    echo "📬 Outgoing messages:"
    cat ~/.agency/queue/outgoing/*.json 2>/dev/null
fi

echo ""
echo "📋 Checking conversations..."
ls -la ~/.agency/queue/conversations/
if [ -f ~/.agency/queue/conversations/*.json ]; then
    echo ""
    echo "💬 Recent conversations:"
    find ~/.agency/queue/conversations -name '*.json' -mmin -5 -exec echo "=== {} ===" \; -exec cat {} \; 2>/dev/null
fi

echo ""
echo "📋 Checking chat files (last 5 minutes)..."
find ~/.agency/queue/chats -name '*.md' -mmin -5 2>/dev/null | while read f; do
    echo "=== $f ==="
    cat "$f"
    echo ""
done || echo "No recent chat files"

echo ""
echo "📋 Checking processor log for conversation history..."
if [ -f "logs/processor.log" ]; then
    echo "Found logs/processor.log"
    grep -E "(Conversation history|History\[|Sending.*tools)" logs/processor.log | tail -20 || echo "No conversation history logs"
fi
