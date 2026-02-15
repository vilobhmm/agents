"""Travel Autopilot System Agent"""

import logging
import re
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.calendar import CalendarIntegration
from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.telegram import TelegramIntegration


logger = logging.getLogger(__name__)


class TravelAutopilotAgent(Agent):
    """Travel Autopilot System Agent"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Travel Autopilot",
            description="I handle end-to-end travel automation: check-ins, boarding passes, transport.",
            proactive=True,
        )

        super().__init__(config, api_key)

        self.email = EmailIntegration()
        self.calendar = CalendarIntegration()
        self.telegram = TelegramIntegration()

        self.flights = []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        logger.info("Monitoring for flight confirmations")

        # Search for flight confirmation emails
        airlines = ["Delta", "United", "American", "Southwest", "JetBlue"]
        flight_emails = []

        for airline in airlines:
            emails = await self.email.search_emails(
                sender=airline, subject="confirmation", max_results=5
            )
            flight_emails.extend(emails)

        logger.info(f"Found {len(flight_emails)} flight emails")

        # Process each flight
        for email_data in flight_emails:
            flight = await self.extract_flight_info(email_data)
            if flight:
                await self.process_flight(flight)

        return {"status": "success", "flights_processed": len(self.flights)}

    async def extract_flight_info(self, email_data: Dict) -> Optional[Dict]:
        """Extract flight information from confirmation email"""

        body = email_data.get("body", "")
        subject = email_data.get("subject", "")

        prompt = f"""Extract flight information from this email:

Subject: {subject}
Body: {body[:2000]}

Extract:
- Confirmation number
- Airline
- Flight number
- Departure airport
- Arrival airport
- Departure date and time
- Arrival date and time
- Passenger name"""

        response = await self.chat(prompt)

        # Parse response
        flight_info = self.parse_flight_response(response)

        if flight_info:
            flight_info["email_id"] = email_data.get("id")

        return flight_info

    def parse_flight_response(self, response: str) -> Optional[Dict]:
        """Parse flight details from response"""

        patterns = {
            "confirmation": r"Confirmation.*?:\s*([A-Z0-9]+)",
            "airline": r"Airline:\s*(.+)",
            "flight_number": r"Flight.*?:\s*([A-Z]{2}\d+)",
            "departure_airport": r"Departure.*?:\s*([A-Z]{3})",
            "arrival_airport": r"Arrival.*?:\s*([A-Z]{3})",
            "departure_time": r"Departure.*?:\s*(.+)",
        }

        flight = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                flight[key] = match.group(1).strip()

        if "confirmation" in flight and "flight_number" in flight:
            return flight

        return None

    async def process_flight(self, flight: Dict):
        """Process a flight booking"""

        confirmation = flight.get("confirmation", "")
        logger.info(f"Processing flight {confirmation}")

        # Add to calendar
        await self.add_to_calendar(flight)

        # Schedule check-in reminder (24 hours before)
        await self.schedule_checkin(flight)

        # Monitor for delays (simplified)
        await self.monitor_flight(flight)

        self.flights.append(flight)

    async def add_to_calendar(self, flight: Dict):
        """Add flight to calendar"""

        departure = flight.get("departure_airport", "")
        arrival = flight.get("arrival_airport", "")
        flight_num = flight.get("flight_number", "")

        # Parse departure time (simplified)
        # In production, use proper date parsing
        start_time = datetime.now() + timedelta(days=7)  # Placeholder

        event_id = await self.calendar.create_event(
            summary=f"✈️ Flight {flight_num}: {departure} → {arrival}",
            start=start_time,
            end=start_time + timedelta(hours=3),
            description=f"Confirmation: {flight.get('confirmation', '')}",
        )

        logger.info(f"Added flight to calendar: {event_id}")

    async def schedule_checkin(self, flight: Dict):
        """Schedule automatic check-in"""

        # In production, integrate with airline APIs
        # For now, send reminder

        message = f"""Flight Check-in Reminder:

Flight: {flight.get('flight_number', '')}
From: {flight.get('departure_airport', '')}
To: {flight.get('arrival_airport', '')}
Confirmation: {flight.get('confirmation', '')}

Check-in opens in 24 hours!"""

        await self.telegram.send_message(message)
        logger.info("Scheduled check-in reminder")

    async def monitor_flight(self, flight: Dict):
        """Monitor flight for delays"""

        # In production, integrate with flight status APIs
        # For now, just log

        logger.info(f"Monitoring flight {flight.get('flight_number', '')}")

    async def handle_delay(self, flight: Dict, new_time: str):
        """Handle flight delay"""

        message = f"""⚠️ Flight Delay Alert!

Flight: {flight.get('flight_number', '')}
New departure time: {new_time}

I'm checking your calendar for conflicts..."""

        await self.telegram.send_message(message)

        # Reschedule meetings if needed
        await self.reschedule_meetings(flight, new_time)

    async def reschedule_meetings(self, flight: Dict, new_time: str):
        """Reschedule meetings affected by delay"""

        # Get events on travel day
        events = await self.calendar.get_events()

        # Send suggestions
        message = "Suggesting meeting reschedules:\n\n"

        for event in events:
            message += f"- {event.get('summary', '')}: Reschedule?\n"

        await self.telegram.send_message(message)
