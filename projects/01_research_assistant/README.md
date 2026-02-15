# Project 1: Personal Research Assistant

An intelligent agent that monitors your reading list and automatically provides summaries and insights.

## Features

- Monitors reading lists from Pocket and Instapaper
- Summarizes key articles overnight
- Sends morning briefings via WhatsApp
- Creates calendar blocks for deep reading sessions
- Generates Notion pages with synthesis notes

## Setup

1. Configure your reading list credentials in `.env`:
   ```
   POCKET_CONSUMER_KEY=your_key
   POCKET_ACCESS_TOKEN=your_token
   INSTAPAPER_USERNAME=your_username
   INSTAPAPER_PASSWORD=your_password
   ```

2. Configure notification preferences:
   ```
   WHATSAPP_RECIPIENT=whatsapp:+1234567890
   ```

3. Configure Notion:
   ```
   NOTION_API_KEY=your_key
   NOTION_DATABASE_ID=your_database_id
   ```

## Usage

```bash
python -m projects.01_research_assistant.main
```

The agent will:
- Run nightly at 2 AM to fetch and summarize articles
- Send morning briefing at 8 AM
- Create calendar blocks for reading time
- Store summaries in Notion

## Configuration

Edit `config.py` to customize:
- Schedule times
- Number of articles to process
- Summary style
- Calendar block duration
