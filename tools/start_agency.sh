#!/bin/bash
# Start complete Agency system (Processor + Telegram Bot)

# Exit on error
set -e

# Activate virtual environment
source agents-venv/bin/activate

# Set environment (properly source .env file)
set -a
source .env
set +a

echo "🚀 Starting Agency System..."
echo ""

# Create logs directory
mkdir -p ~/.agency/logs

# Kill any existing processor
pkill -f "python -m agency.processor" 2>/dev/null || true

# Start processor in background
echo "1️⃣ Starting message processor..."
python -m agency.processor &
PROCESSOR_PID=$!
echo "   ✅ Processor started (PID: $PROCESSOR_PID)"
echo "   📋 Logs: ~/.agency/logs/processor.log"

# Wait for processor to initialize
sleep 3

# Check if processor is still running
if ! ps -p $PROCESSOR_PID > /dev/null; then
    echo "   ❌ Processor failed to start! Check logs:"
    echo "      tail -50 ~/.agency/logs/processor.log"
    exit 1
fi

# Start telegram bot in foreground
echo ""
echo "2️⃣ Starting Telegram bot..."
echo "   Bot will poll for messages and send responses"
echo "   Press Ctrl+C to stop"
echo ""

# Trap Ctrl+C to also kill processor
trap "echo ''; echo 'Stopping...'; kill $PROCESSOR_PID 2>/dev/null; exit" INT TERM

python -m agency.channels.telegram_channel
