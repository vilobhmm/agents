"""
WhatsApp Manager for Avengers System

Provides WhatsApp interface for interacting with Iron Man.
User sends messages → Iron Man responds → Iron Man coordinates other agents
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from openclaw.integrations.whatsapp import WhatsAppIntegration

from .coordination import coordination_hub
from .iron_man import IronManAgent

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("avengers.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

# Flask app for Twilio webhooks
app = Flask(__name__)

# Global Iron Man instance
iron_man: IronManAgent = None
whatsapp: WhatsAppIntegration = None
user_number: str = None


def initialize_iron_man():
    """Initialize Iron Man agent"""
    global iron_man

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found")

    iron_man = IronManAgent(api_key=api_key, coordination=coordination_hub)

    logger.info("🧠 Iron Man initialized and ready")


def initialize_whatsapp():
    """Initialize WhatsApp integration"""
    global whatsapp, user_number

    whatsapp = WhatsAppIntegration()
    user_number = os.getenv("YOUR_WHATSAPP_NUMBER")

    if not user_number:
        raise ValueError(
            "YOUR_WHATSAPP_NUMBER not found. Set it to your WhatsApp number (e.g., whatsapp:+1234567890)"
        )

    logger.info(f"📱 WhatsApp configured for {user_number}")


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Handle incoming WhatsApp messages

    This is the webhook endpoint that Twilio calls when messages arrive.
    """
    global iron_man, whatsapp

    # Get message details
    from_number = request.values.get("From", "")
    message_body = request.values.get("Body", "").strip()

    logger.info(f"📩 Message from {from_number}: {message_body}")

    # Verify it's from authorized user
    if from_number != user_number:
        logger.warning(f"Unauthorized message from {from_number}")
        resp = MessagingResponse()
        resp.message("⚠️ Unauthorized. This bot is for authorized users only.")
        return str(resp)

    # Process message with Iron Man
    try:
        # Run async in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_text = loop.run_until_complete(
            iron_man.handle_user_message(message_body)
        )
        loop.close()

        # Send response
        resp = MessagingResponse()
        resp.message(response_text)

        logger.info(f"📤 Response sent: {response_text[:100]}...")

        return str(resp)

    except Exception as e:
        logger.error(f"Error processing message: {e}")

        resp = MessagingResponse()
        resp.message(f"❌ Error: {str(e)}")
        return str(resp)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "iron_man": "ready" if iron_man else "not initialized",
        "timestamp": datetime.now().isoformat(),
    }


async def send_morning_briefing():
    """Send morning briefing to user"""
    global iron_man, whatsapp, user_number

    logger.info("☀️ Sending morning briefing...")

    briefing = await iron_man.morning_briefing()

    await whatsapp.send_message(to=user_number, body=briefing)

    logger.info("📤 Morning briefing sent")


async def send_evening_summary():
    """Send evening summary to user"""
    global iron_man, whatsapp, user_number

    logger.info("🌙 Sending evening summary...")

    summary = await iron_man.evening_summary()

    await whatsapp.send_message(to=user_number, body=summary)

    logger.info("📤 Evening summary sent")


def start_flask_server():
    """Start Flask webhook server"""
    port = int(os.getenv("PORT", 5000))

    logger.info(f"🚀 Starting WhatsApp webhook server on port {port}")
    logger.info(f"📍 Webhook URL: http://your-server:{ port}/webhook")
    logger.info(
        "⚠️  Configure this URL in Twilio Console → WhatsApp Sandbox → Webhook URL"
    )

    app.run(host="0.0.0.0", port=port, debug=False)


def main():
    """Main entry point"""
    load_dotenv()

    print("\n" + "=" * 60)
    print("🛡⚡ AVENGERS AI OPERATING SYSTEM")
    print("=" * 60)
    print("\nInitializing agents...")

    # Initialize
    initialize_iron_man()
    initialize_whatsapp()

    print("\n✅ Iron Man ready")
    print(f"✅ WhatsApp configured for {user_number}")
    print("\n" + "=" * 60)
    print("🚀 SYSTEM READY")
    print("=" * 60)
    print("\nInteract with Iron Man via WhatsApp!")
    print(f"Send message to: {os.getenv('TWILIO_WHATSAPP_NUMBER', 'your-twilio-number')}")
    print("\nCommands:")
    print("  • status - Get agent statuses")
    print("  • assign <task> - Assign new task")
    print("  • report <agent> - Get agent report")
    print("  • help - Show all commands")
    print("\nWebhook server starting...")
    print("=" * 60 + "\n")

    # Start Flask server (blocking)
    start_flask_server()


if __name__ == "__main__":
    main()
