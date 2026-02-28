#!/bin/bash
# Start Telegram Bot for Agency System

# Activate virtual environment
source agents-venv/bin/activate

# Set environment
export $(cat .env | xargs)

# Start telegram bot
echo "🤖 Starting Telegram bot..."
echo "   Bot will poll Telegram for messages and send responses"
echo "   Press Ctrl+C to stop"
echo ""

python -m agency.channels.telegram_channel
