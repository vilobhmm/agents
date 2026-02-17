#!/bin/bash
# Start complete Agency system (Processor + Telegram Bot)

# Activate virtual environment  
source agents-venv/bin/activate

# Set environment
export $(cat .env | xargs)

echo "🚀 Starting Agency System..."
echo ""

# Start processor in background
echo "1️⃣ Starting message processor..."
nohup python -m agency.processor > logs/processor.log 2>&1 &
PROCESSOR_PID=$!
echo "   ✅ Processor started (PID: $PROCESSOR_PID)"

# Wait a moment
sleep 2

# Start telegram bot in foreground
echo ""
echo "2️⃣ Starting Telegram bot..."
echo "   Bot will poll for messages and send responses"
echo "   Press Ctrl+C to stop"
echo ""

# Trap Ctrl+C to also kill processor
trap "echo ''; echo 'Stopping...'; kill $PROCESSOR_PID 2>/dev/null; exit" INT TERM

python -m agency.channels.telegram_channel
