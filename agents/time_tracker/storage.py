"""
Storage Manager for Time Tracker

Handles persistence of activity data using JSON file storage.
Provides methods for saving, loading, querying, and updating activities.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import uuid


class StorageManager:
    """Manages storage and retrieval of time tracking data."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the Storage Manager.

        Args:
            data_dir: Directory to store data files (defaults to ~/.time_tracker)
        """
        if data_dir is None:
            data_dir = os.path.expanduser('~/.time_tracker')

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.activities_file = self.data_dir / 'activities.json'
        self.metadata_file = self.data_dir / 'metadata.json'

        # Initialize storage if needed
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize storage files if they don't exist."""
        if not self.activities_file.exists():
            self._save_activities([])

        if not self.metadata_file.exists():
            self._save_metadata({
                'created_at': datetime.now().isoformat(),
                'total_activities': 0,
                'last_updated': datetime.now().isoformat()
            })

    def _load_activities(self) -> List[Dict[str, Any]]:
        """Load all activities from storage."""
        try:
            with open(self.activities_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_activities(self, activities: List[Dict[str, Any]]):
        """Save all activities to storage."""
        with open(self.activities_file, 'w') as f:
            json.dump(activities, f, indent=2)

        # Update metadata
        metadata = self._load_metadata()
        metadata['total_activities'] = len(activities)
        metadata['last_updated'] = datetime.now().isoformat()
        self._save_metadata(metadata)

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata."""
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_metadata(self, metadata: Dict[str, Any]):
        """Save metadata."""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    async def save_activity(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a new activity.

        Args:
            activity: Activity data to save

        Returns:
            Saved activity with ID
        """
        activities = self._load_activities()

        # Add unique ID if not present
        if 'id' not in activity:
            activity['id'] = str(uuid.uuid4())

        # Add created timestamp
        if 'created_at' not in activity:
            activity['created_at'] = datetime.now().isoformat()

        activities.append(activity)
        self._save_activities(activities)

        return activity

    async def get_activity_by_id(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific activity by ID.

        Args:
            activity_id: Activity ID

        Returns:
            Activity data or None if not found
        """
        activities = self._load_activities()

        for activity in activities:
            if activity.get('id') == activity_id:
                return activity

        return None

    async def update_activity(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing activity.

        Args:
            activity: Activity data with ID

        Returns:
            Updated activity
        """
        activities = self._load_activities()

        activity_id = activity.get('id')
        if not activity_id:
            raise ValueError("Activity must have an ID to update")

        # Find and update the activity
        for i, existing in enumerate(activities):
            if existing.get('id') == activity_id:
                activity['updated_at'] = datetime.now().isoformat()
                activities[i] = activity
                self._save_activities(activities)
                return activity

        # If not found, save as new
        return await self.save_activity(activity)

    async def delete_activity(self, activity_id: str) -> bool:
        """
        Delete an activity.

        Args:
            activity_id: Activity ID to delete

        Returns:
            True if deleted, False if not found
        """
        activities = self._load_activities()

        initial_count = len(activities)
        activities = [a for a in activities if a.get('id') != activity_id]

        if len(activities) < initial_count:
            self._save_activities(activities)
            return True

        return False

    async def get_all_activities(self) -> List[Dict[str, Any]]:
        """Get all activities."""
        return self._load_activities()

    async def get_activities_by_period(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """
        Get activities within a time period.

        Args:
            start: Period start time
            end: Period end time

        Returns:
            List of activities in the period
        """
        all_activities = self._load_activities()

        filtered = []
        for activity in all_activities:
            activity_start = datetime.fromisoformat(activity['start_time'])

            # Check if activity falls within the period
            if start <= activity_start <= end:
                filtered.append(activity)

        return filtered

    async def get_activities_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all activities in a specific category.

        Args:
            category: Category name

        Returns:
            List of activities in the category
        """
        all_activities = self._load_activities()

        return [
            activity for activity in all_activities
            if activity.get('category') == category
        ]

    async def get_activities_by_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get activities for a specific date.

        Args:
            date: Date to query

        Returns:
            List of activities on that date
        """
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        return await self.get_activities_by_period(start, end)

    async def search_activities(self, query: str) -> List[Dict[str, Any]]:
        """
        Search activities by description.

        Args:
            query: Search query

        Returns:
            List of matching activities
        """
        all_activities = self._load_activities()

        query_lower = query.lower()
        return [
            activity for activity in all_activities
            if query_lower in activity['activity'].lower()
        ]

    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Storage statistics
        """
        metadata = self._load_metadata()
        activities = self._load_activities()

        # Calculate date range
        if activities:
            dates = [datetime.fromisoformat(a['start_time']) for a in activities if a.get('start_time')]
            earliest = min(dates) if dates else None
            latest = max(dates) if dates else None
        else:
            earliest = None
            latest = None

        # Calculate total time tracked
        total_minutes = sum(a.get('duration_minutes', 0) for a in activities)

        return {
            'total_activities': len(activities),
            'total_time_tracked_hours': round(total_minutes / 60, 2),
            'earliest_activity': earliest.isoformat() if earliest else None,
            'latest_activity': latest.isoformat() if latest else None,
            'storage_created': metadata.get('created_at'),
            'last_updated': metadata.get('last_updated'),
            'data_directory': str(self.data_dir)
        }

    async def export_backup(self, backup_path: str) -> Dict[str, Any]:
        """
        Create a backup of all data.

        Args:
            backup_path: Path to save backup

        Returns:
            Backup summary
        """
        activities = self._load_activities()
        metadata = self._load_metadata()

        backup_data = {
            'backup_created': datetime.now().isoformat(),
            'metadata': metadata,
            'activities': activities
        }

        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)

        return {
            'status': 'success',
            'backup_path': backup_path,
            'activities_backed_up': len(activities)
        }

    async def restore_from_backup(self, backup_path: str) -> Dict[str, Any]:
        """
        Restore data from a backup.

        Args:
            backup_path: Path to backup file

        Returns:
            Restore summary
        """
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)

        activities = backup_data.get('activities', [])
        metadata = backup_data.get('metadata', {})

        self._save_activities(activities)
        metadata['restored_at'] = datetime.now().isoformat()
        self._save_metadata(metadata)

        return {
            'status': 'success',
            'activities_restored': len(activities)
        }

    async def clear_all_data(self) -> Dict[str, Any]:
        """
        Clear all activity data (use with caution!).

        Returns:
            Clear operation summary
        """
        activities = self._load_activities()
        count = len(activities)

        self._save_activities([])

        return {
            'status': 'success',
            'activities_cleared': count
        }
