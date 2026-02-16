#!/bin/bash

# Start Agency System with Telegram Integration
# This script starts both the message processor and Telegram bot

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🤖 Starting Agency Multi-Agent System${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo ""
    echo "Please create .env file with:"
    echo "  TELEGRAM_BOT_TOKEN=your-bot-token"
    echo "  TELEGRAM_ALLOWED_USERS=your-user-id"
    echo "  ANTHROPIC_API_KEY=your-api-key"
    echo "  (and other required keys)"
    exit 1
fi

# Load environment variables
echo -e "${GREEN}✓ Loading environment variables...${NC}"
set -a
source .env
set +a

# Check if virtual environment exists
if [ ! -d "agents-venv" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found!${NC}"
    echo ""
    echo "Please create virtual environment first:"
    echo "  python3 -m venv agents-venv"
    echo "  source agents-venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}✓ Activating virtual environment...${NC}"
source agents-venv/bin/activate

# Check required environment variables
echo -e "${GREEN}✓ Checking configuration...${NC}"

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${RED}❌ Error: TELEGRAM_BOT_TOKEN not set in .env${NC}"
    exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Warning: ANTHROPIC_API_KEY not set (required for agents)${NC}"
fi

echo ""
echo -e "${GREEN}✅ Configuration OK!${NC}"
echo ""

# Create logs directory
mkdir -p logs

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down...${NC}"
    kill $PROCESSOR_PID 2>/dev/null || true
    kill $TELEGRAM_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start message processor in background
echo -e "${BLUE}🔄 Starting message processor...${NC}"
python -m agency process > logs/processor.log 2>&1 &
PROCESSOR_PID=$!
echo -e "${GREEN}✓ Message processor started (PID: $PROCESSOR_PID)${NC}"
echo -e "   Logs: logs/processor.log"

# Wait a moment for processor to initialize
sleep 2

# Start Telegram bot
echo -e "${BLUE}📱 Starting Telegram bot...${NC}"
python -m agency.channels.telegram_channel > logs/telegram.log 2>&1 &
TELEGRAM_PID=$!
echo -e "${GREEN}✓ Telegram bot started (PID: $TELEGRAM_PID)${NC}"
echo -e "   Logs: logs/telegram.log"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Agency System Running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Processes:${NC}"
echo -e "  Message Processor: PID $PROCESSOR_PID"
echo -e "  Telegram Bot: PID $TELEGRAM_PID"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Processor: logs/processor.log"
echo -e "  Telegram: logs/telegram.log"
echo ""
echo -e "${BLUE}Monitor logs:${NC}"
echo -e "  tail -f logs/processor.log"
echo -e "  tail -f logs/telegram.log"
echo ""
echo -e "${BLUE}Telegram Bot:${NC}"
echo -e "  Search for your bot on Telegram and send /start"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both processes${NC}"
echo ""

# Wait for either process to exit
wait $PROCESSOR_PID $TELEGRAM_PID
