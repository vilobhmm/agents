"""Persistent storage tools for agents - Memory and state management."""

import logging
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class StorageTools:
    """
    Persistent storage and memory for agents.

    Provides:
    - Key-value storage (preferences, settings)
    - List management (tracked jobs, tasks, contacts)
    - History tracking
    - Search and retrieval
    """

    def __init__(self, agent_id: str, workspace_path: Path):
        """
        Initialize storage for an agent.

        Args:
            agent_id: Agent identifier
            workspace_path: Root workspace directory
        """
        self.agent_id = agent_id
        self.storage_dir = workspace_path / agent_id / "storage"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.kv_file = self.storage_dir / "keyvalue.json"
        self.lists_file = self.storage_dir / "lists.json"
        self.history_file = self.storage_dir / "history.jsonl"

        # Load data
        self.kv_data = self._load_json(self.kv_file, {})
        self.lists_data = self._load_json(self.lists_file, {})

    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Load JSON file with default"""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                return default
        return default

    def _save_json(self, file_path: Path, data: Any):
        """Save JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")

    # ===== Key-Value Storage =====

    def set(self, key: str, value: Any):
        """Set a key-value pair"""
        self.kv_data[key] = value
        self._save_json(self.kv_file, self.kv_data)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key"""
        return self.kv_data.get(key, default)

    def delete(self, key: str):
        """Delete a key"""
        if key in self.kv_data:
            del self.kv_data[key]
            self._save_json(self.kv_file, self.kv_data)

    def get_all(self) -> Dict:
        """Get all key-value pairs"""
        return self.kv_data.copy()

    # ===== List Management =====

    def list_add(self, list_name: str, item: Any):
        """Add item to a list"""
        if list_name not in self.lists_data:
            self.lists_data[list_name] = []

        # Add with timestamp
        self.lists_data[list_name].append({
            "item": item,
            "added_at": datetime.now().isoformat()
        })
        self._save_json(self.lists_file, self.lists_data)

    def list_remove(self, list_name: str, index: int):
        """Remove item from list by index"""
        if list_name in self.lists_data and 0 <= index < len(self.lists_data[list_name]):
            self.lists_data[list_name].pop(index)
            self._save_json(self.lists_file, self.lists_data)

    def list_get(self, list_name: str) -> List:
        """Get all items in a list"""
        return self.lists_data.get(list_name, [])

    def list_clear(self, list_name: str):
        """Clear a list"""
        if list_name in self.lists_data:
            self.lists_data[list_name] = []
            self._save_json(self.lists_file, self.lists_data)

    def list_find(self, list_name: str, search_term: str) -> List:
        """Find items in list containing search term"""
        items = self.lists_data.get(list_name, [])
        results = []

        for idx, entry in enumerate(items):
            item_str = json.dumps(entry["item"]).lower()
            if search_term.lower() in item_str:
                results.append({
                    "index": idx,
                    "item": entry["item"],
                    "added_at": entry["added_at"]
                })

        return results

    # ===== History Tracking =====

    def add_history(self, event_type: str, data: Dict):
        """
        Add an event to history.

        Args:
            event_type: Type of event (e.g., "job_found", "email_sent")
            data: Event data
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }

        try:
            with open(self.history_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Error writing history: {e}")

    def get_history(
        self,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get history events.

        Args:
            event_type: Filter by event type (None for all)
            limit: Maximum number of events to return

        Returns:
            List of history events (most recent first)
        """
        if not self.history_file.exists():
            return []

        events = []
        try:
            with open(self.history_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        if event_type is None or event.get("event_type") == event_type:
                            events.append(event)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.error(f"Error reading history: {e}")

        # Return most recent first
        return events[-limit:][::-1]

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [
            "set", "get", "delete", "get_all",
            "list_add", "list_remove", "list_get", "list_clear", "list_find",
            "add_history", "get_history",
        ]

    def get_tools_description(self) -> str:
        """Get description of available tools for agent prompt"""
        return """
You have access to persistent storage tools:

**Key-Value Storage (preferences, settings):**
- set(key, value) - Store a value
- get(key, default=None) - Retrieve a value
- delete(key) - Delete a key
- get_all() - Get all stored data

**List Management (tracked items):**
- list_add(list_name, item) - Add item to list
- list_remove(list_name, index) - Remove item by index
- list_get(list_name) - Get all items in list
- list_clear(list_name) - Clear a list
- list_find(list_name, search_term) - Search within list

**History Tracking:**
- add_history(event_type, data) - Log an event
- get_history(event_type=None, limit=100) - Get event history

Examples:
- Store user preferences: set("preferred_location", "San Francisco")
- Track jobs: list_add("tracked_jobs", {"title": "ML Engineer", "company": "Anthropic"})
- Log activities: add_history("job_application", {"company": "OpenAI", "role": "Research"})

Use these to remember user preferences and maintain state across conversations!
"""
