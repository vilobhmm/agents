"""
Categorizer Agent

Organizes and categorizes time entries to understand patterns.
Categories include:
- Work (deep work, meetings, emails, admin)
- Personal (errands, chores, socializing)
- Health (exercise, meals, sleep)
- Learning (reading, courses, practice)
- Entertainment (leisure, hobbies)
- Breaks (rest, downtime)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict


class CategorizerAgent:
    """Agent for categorizing and organizing time entries."""

    # Predefined category structure
    CATEGORIES = {
        'work': {
            'deep_work': 'Focused, uninterrupted work on important tasks',
            'meetings': 'Meetings, calls, and collaborations',
            'emails': 'Email and communication',
            'admin': 'Administrative tasks, planning, organizing'
        },
        'personal': {
            'errands': 'Shopping, appointments, life admin',
            'chores': 'Cleaning, cooking, household tasks',
            'social': 'Time with friends, family, socializing'
        },
        'health': {
            'exercise': 'Physical activity and workouts',
            'meals': 'Eating and meal preparation',
            'sleep': 'Rest and sleep',
            'self_care': 'Personal grooming, meditation, etc.'
        },
        'learning': {
            'reading': 'Reading books, articles, documentation',
            'courses': 'Online courses, tutorials, training',
            'practice': 'Hands-on practice and experimentation',
            'research': 'Research and exploration'
        },
        'entertainment': {
            'leisure': 'TV, movies, games, browsing',
            'hobbies': 'Creative hobbies and interests',
            'social_media': 'Social media and casual browsing'
        },
        'breaks': {
            'short_break': 'Short breaks (< 15 min)',
            'long_break': 'Extended breaks and rest',
            'transition': 'Context switching and transitions'
        }
    }

    def __init__(self, storage_manager):
        """
        Initialize the Categorizer Agent.

        Args:
            storage_manager: Storage manager for accessing activity data
        """
        self.storage = storage_manager

    async def categorize_activity(self, activity: Dict[str, Any],
                                  suggested_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Categorize a single activity.

        Args:
            activity: Activity record to categorize
            suggested_category: Optional suggested category

        Returns:
            Activity with category assigned
        """
        if suggested_category:
            activity['category'] = suggested_category
        elif not activity.get('category'):
            # Auto-categorize based on description
            activity['category'] = await self._auto_categorize(activity['activity'])

        # Add subcategory if applicable
        activity['subcategory'] = await self._get_subcategory(
            activity['activity'],
            activity['category']
        )

        # Update in storage
        await self.storage.update_activity(activity)

        return activity

    async def _auto_categorize(self, description: str) -> str:
        """Automatically categorize based on activity description."""
        desc_lower = description.lower()

        # Work indicators
        work_keywords = ['meeting', 'email', 'code', 'coding', 'debug', 'review',
                        'presentation', 'call', 'standup', 'planning', 'design']
        if any(kw in desc_lower for kw in work_keywords):
            return 'work'

        # Learning indicators
        learning_keywords = ['learn', 'study', 'course', 'tutorial', 'reading',
                           'research', 'practice', 'documentation']
        if any(kw in desc_lower for kw in learning_keywords):
            return 'learning'

        # Health indicators
        health_keywords = ['exercise', 'gym', 'workout', 'run', 'yoga', 'walk',
                          'meal', 'lunch', 'dinner', 'breakfast', 'sleep']
        if any(kw in desc_lower for kw in health_keywords):
            return 'health'

        # Break indicators
        break_keywords = ['break', 'rest', 'coffee', 'snack']
        if any(kw in desc_lower for kw in break_keywords):
            return 'breaks'

        # Entertainment indicators
        entertainment_keywords = ['youtube', 'video', 'game', 'movie', 'netflix',
                                'social media', 'browse', 'scrolling', 'tv']
        if any(kw in desc_lower for kw in entertainment_keywords):
            return 'entertainment'

        # Personal indicators
        personal_keywords = ['shopping', 'errands', 'chores', 'cleaning', 'cooking',
                           'laundry', 'groceries']
        if any(kw in desc_lower for kw in personal_keywords):
            return 'personal'

        return 'uncategorized'

    async def _get_subcategory(self, description: str, category: str) -> Optional[str]:
        """Determine subcategory within a category."""
        desc_lower = description.lower()

        if category == 'work':
            if any(kw in desc_lower for kw in ['meeting', 'call', 'standup']):
                return 'meetings'
            elif any(kw in desc_lower for kw in ['email', 'slack', 'message']):
                return 'emails'
            elif any(kw in desc_lower for kw in ['planning', 'organize', 'admin']):
                return 'admin'
            else:
                return 'deep_work'

        elif category == 'health':
            if any(kw in desc_lower for kw in ['exercise', 'gym', 'workout', 'run']):
                return 'exercise'
            elif any(kw in desc_lower for kw in ['meal', 'lunch', 'dinner', 'breakfast', 'eat']):
                return 'meals'
            elif 'sleep' in desc_lower:
                return 'sleep'
            else:
                return 'self_care'

        elif category == 'learning':
            if any(kw in desc_lower for kw in ['read', 'article', 'book']):
                return 'reading'
            elif any(kw in desc_lower for kw in ['course', 'tutorial', 'training']):
                return 'courses'
            elif any(kw in desc_lower for kw in ['practice', 'hands-on', 'experiment']):
                return 'practice'
            else:
                return 'research'

        return None

    async def get_category_breakdown(self, start: datetime, end: datetime) -> Dict[str, Any]:
        """
        Get breakdown of time by category for a period.

        Args:
            start: Period start time
            end: Period end time

        Returns:
            Dictionary with category breakdowns
        """
        activities = await self.storage.get_activities_by_period(start, end)

        # Calculate total time per category
        category_time = defaultdict(float)
        subcategory_time = defaultdict(lambda: defaultdict(float))

        total_time = 0

        for activity in activities:
            duration = activity.get('duration_minutes', 0)
            category = activity.get('category', 'uncategorized')
            subcategory = activity.get('subcategory')

            category_time[category] += duration
            if subcategory:
                subcategory_time[category][subcategory] += duration

            total_time += duration

        # Calculate percentages
        result = {
            'period': {
                'start': start.isoformat(),
                'end': end.isoformat()
            },
            'total_tracked_minutes': round(total_time, 2),
            'total_tracked_hours': round(total_time / 60, 2),
            'categories': {}
        }

        for category, minutes in category_time.items():
            percentage = (minutes / total_time * 100) if total_time > 0 else 0

            result['categories'][category] = {
                'minutes': round(minutes, 2),
                'hours': round(minutes / 60, 2),
                'percentage': round(percentage, 2),
                'subcategories': {}
            }

            # Add subcategory breakdown
            if category in subcategory_time:
                for subcat, subcat_minutes in subcategory_time[category].items():
                    subcat_percentage = (subcat_minutes / minutes * 100) if minutes > 0 else 0
                    result['categories'][category]['subcategories'][subcat] = {
                        'minutes': round(subcat_minutes, 2),
                        'hours': round(subcat_minutes / 60, 2),
                        'percentage': round(subcat_percentage, 2)
                    }

        return result

    async def get_productivity_score(self, start: datetime, end: datetime) -> Dict[str, Any]:
        """
        Calculate productivity score based on time allocation.

        Args:
            start: Period start time
            end: Period end time

        Returns:
            Productivity metrics and score
        """
        breakdown = await self.get_category_breakdown(start, end)

        # Define productivity weights
        productive_categories = {
            'work': 1.0,
            'learning': 0.9,
            'health': 0.7,
            'personal': 0.5
        }

        total_minutes = breakdown['total_tracked_minutes']
        weighted_productive_time = 0

        for category, data in breakdown['categories'].items():
            weight = productive_categories.get(category, 0)
            weighted_productive_time += data['minutes'] * weight

        # Calculate score (0-100)
        productivity_score = (weighted_productive_time / total_minutes * 100) if total_minutes > 0 else 0

        return {
            'period': breakdown['period'],
            'productivity_score': round(productivity_score, 2),
            'total_tracked_time': total_minutes,
            'productive_time_minutes': round(weighted_productive_time, 2),
            'productive_time_hours': round(weighted_productive_time / 60, 2),
            'breakdown_by_productivity': {
                'highly_productive': breakdown['categories'].get('work', {}).get('minutes', 0) +
                                   breakdown['categories'].get('learning', {}).get('minutes', 0),
                'moderately_productive': breakdown['categories'].get('health', {}).get('minutes', 0) +
                                        breakdown['categories'].get('personal', {}).get('minutes', 0),
                'low_productivity': breakdown['categories'].get('entertainment', {}).get('minutes', 0) +
                                   breakdown['categories'].get('breaks', {}).get('minutes', 0)
            }
        }

    async def recategorize_pattern(self, pattern: str, new_category: str) -> int:
        """
        Recategorize all activities matching a pattern.

        Args:
            pattern: Pattern to match in activity descriptions
            new_category: New category to assign

        Returns:
            Number of activities recategorized
        """
        activities = await self.storage.get_all_activities()

        count = 0
        for activity in activities:
            if pattern.lower() in activity['activity'].lower():
                activity['category'] = new_category
                activity['subcategory'] = await self._get_subcategory(
                    activity['activity'],
                    new_category
                )
                await self.storage.update_activity(activity)
                count += 1

        return count

    async def suggest_categories(self) -> Dict[str, List[str]]:
        """
        Return the category structure for user reference.

        Returns:
            Dictionary of categories and subcategories
        """
        return self.CATEGORIES

    async def get_top_activities(self, start: datetime, end: datetime, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the top activities by time spent.

        Args:
            start: Period start time
            end: Period end time
            limit: Number of top activities to return

        Returns:
            List of top activities with time spent
        """
        activities = await self.storage.get_activities_by_period(start, end)

        # Aggregate by activity description
        activity_time = defaultdict(float)
        activity_category = {}

        for activity in activities:
            desc = activity['activity']
            duration = activity.get('duration_minutes', 0)

            activity_time[desc] += duration
            activity_category[desc] = activity.get('category', 'uncategorized')

        # Sort by time spent
        top_activities = sorted(
            activity_time.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        return [
            {
                'activity': activity,
                'total_minutes': round(minutes, 2),
                'total_hours': round(minutes / 60, 2),
                'category': activity_category[activity]
            }
            for activity, minutes in top_activities
        ]
