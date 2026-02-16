"""
Proactive Notification System

Sends automated notifications via Telegram and Email based on:
- Time-based triggers (morning briefings, daily job alerts)
- Event-based triggers (urgent emails, calendar changes, job matches)

No manual checking required - the system keeps you informed!
"""

import asyncio
import logging
import os
import smtplib
from datetime import datetime, time as dtime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, List
import time as pytime

from telegram import Bot

from agency.core.queue import FileQueue
from agency.core.types import MessageData

logger = logging.getLogger(__name__)


class ProactiveNotifier:
    """
    Proactive notification system that sends alerts via Telegram and Email.

    Features:
    - Morning briefings (8am daily)
    - Urgent email alerts (real-time)
    - Calendar reminders (30 min before meetings)
    - Job alerts (daily at 6pm)
    - Email fallback (if Telegram fails)
    """

    def __init__(
        self,
        telegram_bot_token: Optional[str] = None,
        telegram_chat_id: Optional[str] = None,
        email_recipient: Optional[str] = None,
        queue: Optional[FileQueue] = None
    ):
        """
        Initialize proactive notifier.

        Args:
            telegram_bot_token: Telegram bot token
            telegram_chat_id: Your Telegram chat ID
            email_recipient: Your email address
            queue: Message queue for agent invocations
        """
        self.telegram_bot_token = telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = telegram_chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.email_recipient = email_recipient or os.getenv("PROACTIVE_EMAIL")

        self.queue = queue or FileQueue(Path.home() / ".agency" / "queue")

        self.telegram_bot = None
        if self.telegram_bot_token:
            self.telegram_bot = Bot(token=self.telegram_bot_token)

        logger.info("Proactive notifier initialized")

    async def send_telegram(self, message: str) -> bool:
        """Send message via Telegram"""
        if not self.telegram_bot or not self.telegram_chat_id:
            logger.warning("Telegram not configured")
            return False

        try:
            await self.telegram_bot.send_message(
                chat_id=self.telegram_chat_id,
                text=message,
                parse_mode="Markdown"
            )
            logger.info("Telegram notification sent")
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram: {e}")
            return False

    def send_email(self, subject: str, body: str) -> bool:
        """Send notification via Gmail"""
        if not self.email_recipient:
            logger.warning("Email recipient not configured")
            return False

        try:
            # Use Gmail SMTP
            sender_email = os.getenv("GMAIL_USER")
            sender_password = os.getenv("GMAIL_APP_PASSWORD")

            if not sender_email or not sender_password:
                logger.warning("Gmail credentials not configured")
                return False

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = self.email_recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Connect to Gmail
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send email
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent to {self.email_recipient}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    async def notify(self, message: str, subject: Optional[str] = None, email_fallback: bool = True) -> bool:
        """
        Send notification via Telegram, with email fallback.

        Args:
            message: Notification message
            subject: Email subject (if using email)
            email_fallback: Send email if Telegram fails

        Returns:
            True if notification sent successfully
        """
        # Try Telegram first
        success = await self.send_telegram(message)

        # Fallback to email if configured
        if not success and email_fallback:
            email_subject = subject or "Agency Notification"
            success = self.send_email(email_subject, message)

        return success

    async def trigger_agent_task(self, agent_id: str, message: str, sender: str = "proactive"):
        """
        Trigger an agent task via the queue.

        Args:
            agent_id: Agent to invoke
            message: Message/task for agent
            sender: Sender identifier
        """
        message_data = MessageData(
            channel="proactive",
            sender=sender,
            sender_id="proactive_system",
            message=f"@{agent_id} {message}",
            timestamp=pytime.time(),
            message_id=f"proactive_{int(pytime.time())}",
            metadata={
                "proactive": True,
                "telegram_chat_id": self.telegram_chat_id if self.telegram_chat_id else None
            }
        )

        self.queue.enqueue(message_data, "incoming")
        logger.info(f"Queued proactive task for {agent_id}: {message[:50]}...")

    # ===== Scheduled Notifications =====

    async def morning_briefing(self):
        """Send morning briefing (8am daily)"""
        logger.info("Sending morning briefing...")

        # Trigger CC agent to generate briefing
        await self.trigger_agent_task(
            "cc",
            "Give me a comprehensive morning briefing with emails, calendar, priorities, and action items."
        )

        # Wait a moment for processing
        await asyncio.sleep(5)

        # The agent will respond via the queue, which will be sent to Telegram
        # But also send a quick notification
        await self.notify(
            "☀️ **Good Morning!**\n\n"
            "Your daily briefing is being prepared...\n"
            "Check the messages above for details!"
        )

    async def daily_job_alerts(self):
        """Send daily job alerts (6pm daily)"""
        logger.info("Sending daily job alerts...")

        # Trigger job_hunter to check for new jobs
        await self.trigger_agent_task(
            "job_hunter",
            "Check for new job opportunities matching my preferences. Alert me if there are any new matches."
        )

        await self.notify(
            "💼 **Daily Job Alert**\n\n"
            "Checking for new job opportunities...\n"
            "I'll notify you if there are new matches!"
        )

    async def urgent_email_alert(self, email_subject: str, email_sender: str):
        """Alert about urgent email"""
        await self.notify(
            f"🚨 **Urgent Email**\n\n"
            f"From: {email_sender}\n"
            f"Subject: {email_subject}\n\n"
            f"Check your inbox!",
            subject="Urgent Email Alert"
        )

    async def meeting_reminder(self, meeting_title: str, minutes_until: int):
        """Remind about upcoming meeting"""
        await self.notify(
            f"🔔 **Meeting Reminder**\n\n"
            f"**{meeting_title}**\n"
            f"Starts in {minutes_until} minutes\n\n"
            f"Use /meeting for prep details",
            subject=f"Meeting in {minutes_until} min: {meeting_title}"
        )

    async def job_match_alert(self, job_title: str, company: str, job_url: str):
        """Alert about new job match"""
        await self.notify(
            f"💼 **New Job Match!**\n\n"
            f"**{job_title}** at **{company}**\n\n"
            f"🔗 {job_url}\n\n"
            f"This matches your saved preferences!",
            subject=f"New Job Match: {job_title} at {company}"
        )

    async def application_deadline_reminder(self, job_title: str, company: str, days_left: int):
        """Remind about application deadline"""
        await self.notify(
            f"⏰ **Application Deadline**\n\n"
            f"**{job_title}** at **{company}**\n"
            f"Closes in {days_left} days\n\n"
            f"Don't miss out!",
            subject=f"Deadline Alert: {job_title} - {days_left} days left"
        )

    # ===== Scheduler =====

    async def run_scheduler(self):
        """
        Main scheduler loop.

        Runs continuously and triggers notifications at scheduled times.
        """
        logger.info("Starting proactive notification scheduler...")

        morning_briefing_time = dtime(8, 0)  # 8:00 AM
        job_alerts_time = dtime(18, 0)  # 6:00 PM

        morning_sent_today = False
        jobs_sent_today = False

        while True:
            try:
                now = datetime.now()
                current_time = now.time()

                # Morning briefing at 8am
                if (current_time.hour == morning_briefing_time.hour and
                    current_time.minute == morning_briefing_time.minute and
                    not morning_sent_today):

                    await self.morning_briefing()
                    morning_sent_today = True
                    logger.info("Morning briefing sent")

                # Job alerts at 6pm
                if (current_time.hour == job_alerts_time.hour and
                    current_time.minute == job_alerts_time.minute and
                    not jobs_sent_today):

                    await self.daily_job_alerts()
                    jobs_sent_today = True
                    logger.info("Job alerts sent")

                # Reset flags at midnight
                if current_time.hour == 0 and current_time.minute == 0:
                    morning_sent_today = False
                    jobs_sent_today = False
                    logger.info("Daily flags reset")

                # Check every minute
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Error in scheduler: {e}", exc_info=True)
                await asyncio.sleep(60)


async def main():
    """Run proactive notification scheduler"""
    import sys
    from dotenv import load_dotenv

    # Load environment
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get Telegram chat ID from environment
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        logger.error("TELEGRAM_CHAT_ID not set in .env")
        logger.info("To get your chat ID:")
        logger.info("1. Send a message to your bot on Telegram")
        logger.info("2. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
        logger.info("3. Look for 'chat':{'id': YOUR_CHAT_ID}")
        logger.info("4. Add to .env: TELEGRAM_CHAT_ID=your-chat-id")
        sys.exit(1)

    # Create notifier
    notifier = ProactiveNotifier()

    logger.info("🚀 Proactive notification system starting...")
    logger.info(f"   Telegram chat ID: {chat_id}")
    logger.info(f"   Email recipient: {notifier.email_recipient}")
    logger.info("")
    logger.info("📋 Schedule:")
    logger.info("   Morning briefing: 8:00 AM daily")
    logger.info("   Job alerts: 6:00 PM daily")
    logger.info("")
    logger.info("Press Ctrl+C to stop")
    logger.info("")

    # Run scheduler
    await notifier.run_scheduler()


if __name__ == "__main__":
    asyncio.run(main())
