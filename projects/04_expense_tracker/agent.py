"""Smart Expense Tracker Agent"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from openclaw.core.agent import Agent, AgentConfig
from openclaw.integrations.email import EmailIntegration
from openclaw.integrations.notion import NotionIntegration
from openclaw.integrations.whatsapp import WhatsAppIntegration
from openclaw.tools.ocr import OCRProcessor


logger = logging.getLogger(__name__)


class ExpenseTrackerAgent(Agent):
    """Smart Expense Tracker Agent"""

    def __init__(self, api_key: str = None):
        config = AgentConfig(
            name="Expense Tracker",
            description="I process receipts, categorize expenses, and track spending.",
            proactive=True,
        )

        super().__init__(config, api_key)

        self.email = EmailIntegration()
        self.notion = NotionIntegration()
        self.whatsapp = WhatsAppIntegration()
        self.ocr = OCRProcessor()

        self.expenses = []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        logger.info("Processing expense emails")

        # Search for receipt/invoice emails
        keywords = ["receipt", "invoice", "payment confirmation"]
        all_emails = []

        for keyword in keywords:
            emails = await self.email.search_emails(subject=keyword, max_results=20)
            all_emails.extend(emails)

        logger.info(f"Found {len(all_emails)} potential expense emails")

        # Process each email
        processed = 0
        for email_data in all_emails:
            expense = await self.extract_expense(email_data)
            if expense:
                await self.record_expense(expense)
                processed += 1

        return {"status": "success", "expenses_processed": processed}

    async def extract_expense(self, email_data: Dict) -> Optional[Dict]:
        """Extract expense information from email"""

        subject = email_data.get("subject", "")
        body = email_data.get("body", "")
        sender = email_data.get("from", "")

        # Use Claude to extract expense details
        prompt = f"""Extract expense information from this email:

Subject: {subject}
From: {sender}
Body: {body[:1000]}

Extract and return in this format:
- Amount: [amount with currency]
- Merchant: [merchant name]
- Date: [date]
- Category: [category like Food, Transport, Shopping, Utilities, etc.]
- Description: [brief description]"""

        response = await self.chat(prompt)

        # Parse response
        expense = self.parse_expense_response(response)
        if expense:
            expense["email_id"] = email_data.get("id")
            expense["source"] = "email"

        return expense

    def parse_expense_response(self, response: str) -> Optional[Dict]:
        """Parse expense details from Claude's response"""

        patterns = {
            "amount": r"Amount:\s*\$?([\d,]+\.?\d*)",
            "merchant": r"Merchant:\s*(.+)",
            "date": r"Date:\s*(.+)",
            "category": r"Category:\s*(.+)",
            "description": r"Description:\s*(.+)",
        }

        expense = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                expense[key] = match.group(1).strip()

        # Validate we have minimum required fields
        if "amount" in expense and "merchant" in expense:
            return expense

        return None

    async def record_expense(self, expense: Dict):
        """Record expense in Notion"""

        # Create Notion page
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": f"{expense.get('merchant', 'Unknown')} - ${expense.get('amount', '0')}"
                        }
                    }
                ]
            },
            "Amount": {"number": float(expense.get("amount", "0").replace(",", ""))},
            "Merchant": {"rich_text": [{"text": {"content": expense.get("merchant", "")}}]},
            "Category": {"select": {"name": expense.get("category", "Other")}},
            "Date": {
                "date": {"start": expense.get("date", datetime.now().isoformat())}
            },
        }

        children = [
            self.notion.create_heading_block(expense.get("merchant", "Expense"), level=1),
            self.notion.create_text_block(f"Amount: ${expense.get('amount', '0')}"),
            self.notion.create_text_block(f"Category: {expense.get('category', 'Other')}"),
            self.notion.create_text_block(f"Description: {expense.get('description', '')}"),
        ]

        page_id = await self.notion.create_page(properties=properties, children=children)

        if page_id:
            self.expenses.append(expense)
            logger.info(f"Recorded expense: {expense.get('merchant')} - ${expense.get('amount')}")

    async def send_weekly_report(self):
        """Send weekly spending report"""

        if not self.expenses:
            return

        # Calculate totals by category
        categories = {}
        total = 0

        for expense in self.expenses:
            category = expense.get("category", "Other")
            amount = float(expense.get("amount", "0").replace(",", ""))

            categories[category] = categories.get(category, 0) + amount
            total += amount

        # Format report
        report = "Weekly Spending Report:\n\n"
        report += f"Total: ${total:.2f}\n\n"
        report += "By Category:\n"

        for category, amount in sorted(
            categories.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (amount / total) * 100
            report += f"- {category}: ${amount:.2f} ({percentage:.1f}%)\n"

        # Send via WhatsApp
        await self.whatsapp.send_message(os.getenv("WHATSAPP_RECIPIENT"), report)
        logger.info("Sent weekly spending report")

        # Clear processed expenses
        self.expenses = []
