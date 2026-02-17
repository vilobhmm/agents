# Telegram Bot Setup - QUICK START

## 🎯 The Problem

You have been running ONLY the processor (PID 9055), but you need BOTH services:

1. **Processor** - Picks up messages from incoming queue, processes them, puts responses in outgoing queue
2. **Telegram Bot** - Receives messages from Telegram → incoming queue, polls outgoing queue → sends to Telegram

## ✅ Solution

### Option 1: Start Everything (Recommended)

```bash
cd ~/path/to/agents  # YOUR agents directory on Mac
./start_agency.sh
```

This starts:
- Processor (background)
- Telegram bot (foreground)

Press Ctrl+C to stop both.

### Option 2: Manual Start

**Terminal 1 - Processor:**
```bash
cd ~/path/to/agents
source agents-venv/bin/activate
python -m agency.processor
```

**Terminal 2 - Telegram Bot:**
```bash
cd ~/path/to/agents
source agents-venv/bin/activate
python -m agency.channels.telegram_channel
```

## 📱 Test It

1. Open Telegram
2. Find your bot (@your_bot_name)
3. Send: `/calendar`
4. You should get a response!

## 🔍 Verify It's Working

Check both processes are running:
```bash
ps aux | grep -E "(processor|telegram)" | grep -v grep
```

You should see:
- `python -m agency.processor`
- `python -m agency.channels.telegram_channel`

## 📋 What Each Component Does

```
Telegram Message → Telegram Bot → Incoming Queue
                                       ↓
                                   Processor
                                       ↓
                              Outgoing Queue → Telegram Bot → Telegram Response
```

## 🐛 Troubleshooting

**"403 Forbidden" error:**
- Check your TELEGRAM_BOT_TOKEN in .env
- Verify internet connection
- Try: `curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe`

**No response from bot:**
- Check both services are running
- Check logs/processor.log for errors
- Send `/status` to bot to check if it's alive

**Messages processed but no Telegram response:**
- This was YOUR issue! The processor was running but telegram bot wasn't!
- Start the telegram bot with instructions above
