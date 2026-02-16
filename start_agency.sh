#!/bin/bash
# Quick start script for Agency system

set -e

echo "🚀 Starting Agency System"
echo "========================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env with required variables:"
    echo ""
    echo "ANTHROPIC_API_KEY=your_key_here"
    echo "TELEGRAM_BOT_TOKEN=your_token_here"
    echo "TELEGRAM_ALLOWED_USERS=your_user_id_here"
    echo ""
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
source .env
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set in .env"
    exit 1
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  TELEGRAM_BOT_TOKEN not set - Telegram bot will not work"
fi

echo "✅ Environment variables loaded"
echo ""

# Stop any running instances
echo "Stopping any existing agency processes..."
python -m agency stop 2>/dev/null || true
echo ""

# Start the agency
echo "Starting agency (processor + Telegram)..."
echo ""
echo "Press Ctrl+C to stop"
echo ""

python -m agency start

echo ""
echo "👋 Agency stopped"
