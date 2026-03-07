"""
Voice-Interactive Time Tracker Extension

Enables natural voice/text interaction with the time tracker:
- "I'm working on X"
- "I didn't get to X"
- "I completed X"
- "What should I do next?"
- "What am I supposed to be doing now?"
- Tracks reality vs. scheduled plans
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re


class VoiceInteractiveTracker:
    """Voice/conversational interface for the time tracker."""

    def __init__(self, time_tracker_coordinator):
        """
        Initialize voice-interactive tracker.

        Args:
            time_tracker_coordinator: Main time tracker coordinator
        """
        self.tracker = time_tracker_coordinator
        self.conversation_history = []
        self.scheduled_activities = []  # Planned activities
        self.action_log = []  # Actual actions taken

    async def process_voice_input(self, text: str) -> Dict[str, Any]:
        """
        Process natural language input and take appropriate action.

        Args:
            text: Natural language input from user

        Returns:
            Response with action taken and message

        Examples:
            "I'm working on documentation" -> starts activity
            "I finished the meeting" -> stops activity
            "What should I do next?" -> suggests next activity
        """
        text_lower = text.lower().strip()

        # Log to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_input': text,
            'type': 'user'
        })

        # Detect intent and extract information
        response = await self._parse_and_execute(text_lower, text)

        # Log response
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'response': response,
            'type': 'agent'
        })

        return response

    async def _parse_and_execute(self, text_lower: str, original_text: str) -> Dict[str, Any]:
        """Parse user input and execute appropriate action."""

        # Starting activities
        if any(phrase in text_lower for phrase in ['working on', 'starting', 'beginning', "i'm doing"]):
            return await self._handle_start_activity(original_text)

        # Completed activities
        elif any(phrase in text_lower for phrase in ['finished', 'completed', 'done with', 'wrapped up']):
            return await self._handle_completed_activity(original_text)

        # Didn't get to something
        elif any(phrase in text_lower for phrase in ["didn't get to", "couldn't do", "skipped", "missed"]):
            return await self._handle_missed_activity(original_text)

        # What should I do next?
        elif any(phrase in text_lower for phrase in ['what should i do', 'what next', "what's next", 'what now']):
            return await self._handle_what_next()

        # What am I supposed to be doing?
        elif any(phrase in text_lower for phrase in ['supposed to be', 'scheduled for', 'planned to']):
            return await self._handle_whats_scheduled()

        # Quick status check
        elif any(phrase in text_lower for phrase in ['how am i doing', 'my progress', 'status', 'summary']):
            return await self._handle_status_check()

        # Taking a break
        elif any(phrase in text_lower for phrase in ['taking a break', 'break time', 'stepping away']):
            return await self._handle_break()

        # Deviation from plan
        elif 'instead' in text_lower or 'actually' in text_lower:
            return await self._handle_deviation(original_text)

        # Default: try to extract activity and start tracking
        else:
            return await self._handle_default(original_text)

    async def _handle_start_activity(self, text: str) -> Dict[str, Any]:
        """Handle 'I'm working on X' type inputs."""
        # Extract activity name
        activity = self._extract_activity(text)

        if not activity:
            return {
                'action': 'clarification_needed',
                'message': "I couldn't quite catch what you're working on. Could you tell me more specifically?"
            }

        # Start tracking
        result = await self.tracker.start_activity(activity)

        # Log action
        self.action_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'started',
            'activity': activity,
            'scheduled': await self._was_scheduled(activity),
            'category': result.get('category')
        })

        # Check if this was scheduled
        scheduled_match = await self._check_scheduled_match(activity)

        if scheduled_match:
            message = f"✅ Started tracking: **{activity}** (as scheduled!)\nCategory: {result['category']}"
        else:
            scheduled = await self._get_current_scheduled()
            if scheduled:
                message = f"✅ Started tracking: **{activity}**\nCategory: {result['category']}\n\n📅 Note: You were scheduled for '{scheduled['activity']}' at this time."
            else:
                message = f"✅ Started tracking: **{activity}**\nCategory: {result['category']}"

        return {
            'action': 'started_activity',
            'activity': activity,
            'category': result['category'],
            'message': message,
            'on_schedule': bool(scheduled_match)
        }

    async def _handle_completed_activity(self, text: str) -> Dict[str, Any]:
        """Handle 'I finished X' type inputs."""
        activity = self._extract_activity(text)

        # Stop current activity
        completed = await self.tracker.stop_activity()

        if completed:
            duration = completed.get('duration_minutes', 0)

            # Log completion
            self.action_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'completed',
                'activity': completed['activity'],
                'duration_minutes': duration
            })

            message = f"✅ Completed: **{completed['activity']}**\nDuration: {duration:.0f} minutes ({duration/60:.1f} hours)"

            # Suggest what's next
            next_up = await self._suggest_next_activity()
            if next_up:
                message += f"\n\n💡 Up next: {next_up}"

            return {
                'action': 'completed_activity',
                'activity': completed['activity'],
                'duration_minutes': duration,
                'message': message,
                'next_suggestion': next_up
            }
        else:
            return {
                'action': 'no_activity',
                'message': "I don't have any active activity to complete. Want to log something you just finished?"
            }

    async def _handle_missed_activity(self, text: str) -> Dict[str, Any]:
        """Handle 'I didn't get to X' type inputs."""
        activity = self._extract_activity(text)

        if not activity:
            return {
                'action': 'clarification_needed',
                'message': "What didn't you get to? I'll make a note of it."
            }

        # Log the miss
        self.action_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'missed',
            'activity': activity,
            'reason': 'user_reported'
        })

        # Remove from scheduled if present
        self._remove_from_scheduled(activity)

        message = f"📝 Noted: You didn't get to **{activity}**.\n\nWould you like me to:\n• Reschedule it for later?\n• Remove it from your plan?\n• Just keep it noted?"

        return {
            'action': 'missed_activity',
            'activity': activity,
            'message': message
        }

    async def _handle_what_next(self) -> Dict[str, Any]:
        """Handle 'What should I do next?' type inputs."""
        # Check scheduled activities
        scheduled = await self._get_next_scheduled()

        # Get suggestions based on current time and patterns
        suggestions = await self._get_smart_suggestions()

        message = "🤔 Here's what I suggest:\n\n"

        if scheduled:
            message += f"📅 **Scheduled next:** {scheduled['activity']}\n"
            if scheduled.get('start_time'):
                message += f"   Time: {scheduled['start_time']}\n"

        if suggestions:
            message += "\n💡 **Smart suggestions:**\n"
            for i, suggestion in enumerate(suggestions[:3], 1):
                message += f"{i}. {suggestion['activity']} ({suggestion['reason']})\n"

        # Check gaps
        gaps = await self.tracker.fill_gaps()
        if gaps:
            message += f"\n⚠️ You have {len(gaps)} time gap(s) to fill in."

        return {
            'action': 'suggestion',
            'scheduled': scheduled,
            'suggestions': suggestions,
            'message': message
        }

    async def _handle_whats_scheduled(self) -> Dict[str, Any]:
        """Handle 'What am I supposed to be doing?' type inputs."""
        current = await self._get_current_scheduled()
        upcoming = await self._get_upcoming_scheduled(hours=2)

        message = ""

        if current:
            message = f"📅 **Right now:** {current['activity']}\n"
            if current.get('duration'):
                message += f"   Planned duration: {current['duration']} min\n"
        else:
            message = "🆓 You don't have anything scheduled right now.\n"

        if upcoming:
            message += "\n📋 **Coming up:**\n"
            for activity in upcoming[:3]:
                start_time = activity.get('start_time', 'Soon')
                message += f"• {activity['activity']} ({start_time})\n"

        # Check if currently tracking matches schedule
        current_activity = await self.tracker.what_am_i_doing()
        if current_activity and current:
            if current_activity['activity'].lower() != current['activity'].lower():
                message += f"\n⚠️ **Note:** You're currently tracking '{current_activity['activity']}' but scheduled for '{current['activity']}'"

        return {
            'action': 'schedule_info',
            'current_scheduled': current,
            'upcoming_scheduled': upcoming,
            'message': message
        }

    async def _handle_status_check(self) -> Dict[str, Any]:
        """Handle 'How am I doing?' type inputs."""
        # Get today's summary
        summary = await self.tracker.analytics.get_daily_summary()

        # Calculate schedule adherence
        adherence = await self._calculate_schedule_adherence()

        # Get productivity score
        score = await self.tracker.productivity_score(days=1)

        message = f"""📊 **Your Status Update:**

⏰ **Time tracked today:** {summary['total_tracked_hours']:.1f} hours
📈 **Productivity score:** {score['productivity_score']:.0f}/100
✅ **Schedule adherence:** {adherence['percentage']:.0f}%

📋 **Activities today:** {summary['activity_count']}
🎯 **Focus score:** {await self._get_focus_score():.0f}%

"""

        # Add top activities
        if summary.get('top_activities'):
            message += "**Top activities:**\n"
            for activity, mins in summary['top_activities'][:3]:
                message += f"• {activity}: {mins/60:.1f}h\n"

        return {
            'action': 'status',
            'summary': summary,
            'productivity_score': score['productivity_score'],
            'adherence': adherence,
            'message': message
        }

    async def _handle_break(self) -> Dict[str, Any]:
        """Handle 'Taking a break' type inputs."""
        result = await self.tracker.start_activity("Break", "breaks")

        return {
            'action': 'break_started',
            'message': "✅ Enjoy your break! Let me know when you're back. 😊"
        }

    async def _handle_deviation(self, text: str) -> Dict[str, Any]:
        """Handle 'I was scheduled for X but did Y instead'."""
        # Extract what was scheduled and what actually happened
        scheduled = self._extract_scheduled_activity(text)
        actual = self._extract_actual_activity(text)

        if actual:
            result = await self.tracker.start_activity(actual)

            message = f"✅ Tracking: **{actual}**\n\n"

            if scheduled:
                message += f"📝 Noted: You deviated from '{scheduled}'\n"
                # Log the deviation
                self.action_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'deviation',
                    'scheduled': scheduled,
                    'actual': actual
                })

            message += f"That's totally fine! Flexibility is important. Should I reschedule '{scheduled}' for later?"

            return {
                'action': 'deviation_logged',
                'scheduled': scheduled,
                'actual': actual,
                'message': message
            }

        return {
            'action': 'clarification_needed',
            'message': "What are you actually working on now?"
        }

    async def _handle_default(self, text: str) -> Dict[str, Any]:
        """Default handler - try to extract activity and start tracking."""
        activity = self._extract_activity(text)

        if activity and len(activity) > 3:
            result = await self.tracker.start_activity(activity)
            return {
                'action': 'started_activity',
                'activity': activity,
                'message': f"✅ Started tracking: **{activity}**\n(If this isn't right, just tell me what you're actually doing!)"
            }

        return {
            'action': 'unclear',
            'message': "I'm not quite sure what you mean. Could you tell me:\n• What you're working on\n• What you just finished\n• Or what you need help with?"
        }

    def _extract_activity(self, text: str) -> Optional[str]:
        """Extract activity name from natural language text."""
        # Remove common phrases
        text = text.lower()

        patterns = [
            r"(?:working on|starting|beginning|doing)\s+(.+)",
            r"(?:finished|completed|done with)\s+(.+)",
            r"(?:didn't get to|couldn't do|skipped|missed)\s+(.+)",
            r"^i'm\s+(.+)",
            r"^i\s+(.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                activity = match.group(1).strip()
                # Clean up
                activity = activity.replace("the ", "").replace(" now", "").strip()
                return activity.capitalize() if activity else None

        # If no pattern matches, return cleaned text if it's substantial
        cleaned = text.strip()
        if len(cleaned) > 5 and not any(word in cleaned for word in ['what', 'how', 'when', 'should', '?']):
            return cleaned.capitalize()

        return None

    def _extract_scheduled_activity(self, text: str) -> Optional[str]:
        """Extract what was scheduled from deviation text."""
        patterns = [
            r"scheduled for\s+(.+?)(?:\s+but|\s+instead)",
            r"supposed to\s+(.+?)(?:\s+but|\s+instead)",
            r"planned to\s+(.+?)(?:\s+but|\s+instead)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip().capitalize()

        return None

    def _extract_actual_activity(self, text: str) -> Optional[str]:
        """Extract what actually happened from deviation text."""
        patterns = [
            r"(?:but|instead|actually)\s+(?:did|doing|worked on)\s+(.+)",
            r"(?:but|instead|actually)\s+(.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                activity = match.group(1).strip()
                return activity.capitalize() if activity else None

        return None

    async def _was_scheduled(self, activity: str) -> bool:
        """Check if an activity was scheduled."""
        for scheduled in self.scheduled_activities:
            if scheduled['activity'].lower() in activity.lower() or activity.lower() in scheduled['activity'].lower():
                return True
        return False

    async def _check_scheduled_match(self, activity: str) -> Optional[Dict]:
        """Check if activity matches current schedule."""
        current = await self._get_current_scheduled()
        if current:
            if current['activity'].lower() in activity.lower() or activity.lower() in current['activity'].lower():
                return current
        return None

    async def _get_current_scheduled(self) -> Optional[Dict]:
        """Get currently scheduled activity."""
        now = datetime.now()

        for activity in self.scheduled_activities:
            start = datetime.fromisoformat(activity['start_time'])
            end = start + timedelta(minutes=activity.get('duration', 60))

            if start <= now <= end:
                return activity

        return None

    async def _get_next_scheduled(self) -> Optional[Dict]:
        """Get next scheduled activity."""
        now = datetime.now()

        upcoming = [
            a for a in self.scheduled_activities
            if datetime.fromisoformat(a['start_time']) > now
        ]

        if upcoming:
            return sorted(upcoming, key=lambda x: x['start_time'])[0]

        return None

    async def _get_upcoming_scheduled(self, hours: int = 2) -> List[Dict]:
        """Get activities scheduled in next N hours."""
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)

        upcoming = [
            a for a in self.scheduled_activities
            if now < datetime.fromisoformat(a['start_time']) <= cutoff
        ]

        return sorted(upcoming, key=lambda x: x['start_time'])

    async def _suggest_next_activity(self) -> Optional[str]:
        """Suggest what to do next based on schedule and patterns."""
        # Check scheduled
        scheduled = await self._get_next_scheduled()
        if scheduled:
            return scheduled['activity']

        # Check gaps
        gaps = await self.tracker.fill_gaps()
        if gaps:
            return "Fill in your recent time gaps"

        # Smart suggestions based on time of day and patterns
        suggestions = await self._get_smart_suggestions()
        if suggestions:
            return suggestions[0]['activity']

        return None

    async def _get_smart_suggestions(self) -> List[Dict]:
        """Get smart activity suggestions based on context."""
        now = datetime.now()
        hour = now.hour

        suggestions = []

        # Time-based suggestions
        if 9 <= hour < 12:
            suggestions.append({'activity': 'Deep work session', 'reason': 'Peak morning productivity'})
        elif 14 <= hour < 17:
            suggestions.append({'activity': 'Meetings or collaboration', 'reason': 'Afternoon energy'})
        elif hour >= 17:
            suggestions.append({'activity': 'Email catchup', 'reason': 'End of day admin'})

        # Pattern-based suggestions (would use actual historical data)
        patterns = await self.tracker.productivity_patterns(days=7)
        if patterns:
            # Add suggestions based on patterns
            pass

        return suggestions

    async def _calculate_schedule_adherence(self) -> Dict[str, Any]:
        """Calculate how well user is following schedule."""
        total_scheduled = len(self.scheduled_activities)
        if total_scheduled == 0:
            return {'percentage': 100, 'on_track': 0, 'deviated': 0}

        on_track = sum(1 for log in self.action_log if log.get('scheduled', False))
        deviated = sum(1 for log in self.action_log if log.get('action') == 'deviation')

        percentage = (on_track / total_scheduled * 100) if total_scheduled > 0 else 0

        return {
            'percentage': percentage,
            'on_track': on_track,
            'deviated': deviated,
            'total_scheduled': total_scheduled
        }

    async def _get_focus_score(self) -> float:
        """Get today's focus score."""
        metrics = await self.tracker.focus_metrics()
        return metrics.get('focus_score', 0)

    def _remove_from_scheduled(self, activity: str):
        """Remove activity from schedule."""
        self.scheduled_activities = [
            a for a in self.scheduled_activities
            if activity.lower() not in a['activity'].lower()
        ]

    async def add_scheduled_activity(self, activity: str, start_time: datetime,
                                    duration: int = 60, category: str = None):
        """
        Add a scheduled activity to the plan.

        Args:
            activity: Activity description
            start_time: When it's scheduled
            duration: Duration in minutes
            category: Optional category
        """
        self.scheduled_activities.append({
            'activity': activity,
            'start_time': start_time.isoformat(),
            'duration': duration,
            'category': category
        })

    async def get_reality_vs_plan(self) -> Dict[str, Any]:
        """Compare what was planned vs what actually happened."""
        # Get all scheduled activities for today
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_scheduled = [
            a for a in self.scheduled_activities
            if today_start <= datetime.fromisoformat(a['start_time']) <= datetime.now()
        ]

        # Get actual activities
        actual = await self.tracker.get_today()

        # Compare
        matched = []
        missed = []
        unplanned = []

        for scheduled in today_scheduled:
            found = False
            for act in actual:
                if scheduled['activity'].lower() in act['activity'].lower():
                    matched.append({
                        'scheduled': scheduled,
                        'actual': act,
                        'status': 'completed'
                    })
                    found = True
                    break

            if not found:
                missed.append(scheduled)

        # Find unplanned activities
        scheduled_names = [s['activity'].lower() for s in today_scheduled]
        for act in actual:
            if not any(name in act['activity'].lower() for name in scheduled_names):
                unplanned.append(act)

        return {
            'matched': matched,
            'missed': missed,
            'unplanned': unplanned,
            'adherence_score': (len(matched) / len(today_scheduled) * 100) if today_scheduled else 100
        }

    async def get_conversation_summary(self) -> str:
        """Get a summary of the conversation history."""
        if not self.conversation_history:
            return "No conversation history yet."

        summary = f"**Conversation Summary** ({len(self.conversation_history)} interactions)\n\n"

        # Show last 5 interactions
        recent = self.conversation_history[-10:]

        for interaction in recent:
            time = datetime.fromisoformat(interaction['timestamp']).strftime('%H:%M')

            if interaction['type'] == 'user':
                summary += f"🗣️ **You** ({time}): {interaction['user_input']}\n"
            else:
                response = interaction['response']
                summary += f"🤖 **Agent** ({time}): {response.get('action', 'response')}\n\n"

        return summary
