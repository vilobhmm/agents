"""Proactive scheduler for OpenClaw agents"""

import asyncio
import logging
from datetime import datetime
from typing import Callable, Dict, List, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from openclaw.core.agent import Agent


logger = logging.getLogger(__name__)


class ProactiveScheduler:
    """Scheduler for proactive agent execution"""

    def __init__(self, timezone: str = "UTC"):
        self.scheduler = AsyncIOScheduler(timezone=timezone)
        self.jobs: Dict[str, str] = {}  # agent_name -> job_id
        self.running = False
        logger.info(f"Initialized ProactiveScheduler with timezone: {timezone}")

    def schedule_agent(
        self,
        agent: Agent,
        trigger: str,
        trigger_type: str = "cron",
        job_id: Optional[str] = None,
    ):
        """
        Schedule an agent to run proactively.

        Args:
            agent: Agent to schedule
            trigger: Cron expression or interval specification
            trigger_type: 'cron' or 'interval'
            job_id: Optional job ID (defaults to agent name)
        """
        job_id = job_id or agent.config.name

        if trigger_type == "cron":
            # Parse cron expression
            # Format: minute hour day month day_of_week
            trigger_obj = CronTrigger.from_crontab(trigger)
        elif trigger_type == "interval":
            # Parse interval (e.g., "5m", "1h", "30s")
            unit = trigger[-1]
            value = int(trigger[:-1])

            kwargs = {}
            if unit == "s":
                kwargs["seconds"] = value
            elif unit == "m":
                kwargs["minutes"] = value
            elif unit == "h":
                kwargs["hours"] = value
            elif unit == "d":
                kwargs["days"] = value
            else:
                raise ValueError(f"Invalid interval unit: {unit}")

            trigger_obj = IntervalTrigger(**kwargs)
        else:
            raise ValueError(f"Invalid trigger type: {trigger_type}")

        # Add job
        self.scheduler.add_job(
            self._run_agent,
            trigger=trigger_obj,
            args=[agent],
            id=job_id,
            replace_existing=True,
        )

        self.jobs[agent.config.name] = job_id
        logger.info(
            f"Scheduled agent '{agent.config.name}' with {trigger_type} trigger: {trigger}"
        )

    async def _run_agent(self, agent: Agent):
        """Run an agent (internal method)"""
        try:
            logger.info(f"Running scheduled agent: {agent.config.name}")
            result = await agent.process({})
            logger.info(f"Scheduled agent completed: {agent.config.name}")

            # Execute callbacks
            for callback in agent.callbacks:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(result)
                    else:
                        callback(result)
                except Exception as e:
                    logger.error(f"Error in callback: {e}")

        except Exception as e:
            logger.error(f"Error running scheduled agent {agent.config.name}: {e}")

    def schedule_function(
        self,
        func: Callable,
        trigger: str,
        trigger_type: str = "cron",
        job_id: Optional[str] = None,
        **kwargs,
    ):
        """
        Schedule a function to run proactively.

        Args:
            func: Function to schedule
            trigger: Cron expression or interval specification
            trigger_type: 'cron' or 'interval'
            job_id: Optional job ID
            **kwargs: Additional arguments to pass to the function
        """
        if not job_id:
            job_id = f"func_{func.__name__}_{datetime.now().timestamp()}"

        if trigger_type == "cron":
            trigger_obj = CronTrigger.from_crontab(trigger)
        elif trigger_type == "interval":
            unit = trigger[-1]
            value = int(trigger[:-1])

            kwargs_trigger = {}
            if unit == "s":
                kwargs_trigger["seconds"] = value
            elif unit == "m":
                kwargs_trigger["minutes"] = value
            elif unit == "h":
                kwargs_trigger["hours"] = value
            elif unit == "d":
                kwargs_trigger["days"] = value

            trigger_obj = IntervalTrigger(**kwargs_trigger)
        else:
            raise ValueError(f"Invalid trigger type: {trigger_type}")

        self.scheduler.add_job(
            func, trigger=trigger_obj, kwargs=kwargs, id=job_id, replace_existing=True
        )

        logger.info(f"Scheduled function '{func.__name__}' with job ID: {job_id}")
        return job_id

    def unschedule_agent(self, agent_name: str):
        """Remove an agent from the schedule"""
        job_id = self.jobs.get(agent_name)
        if job_id:
            self.scheduler.remove_job(job_id)
            del self.jobs[agent_name]
            logger.info(f"Unscheduled agent: {agent_name}")
        else:
            logger.warning(f"Agent not found in schedule: {agent_name}")

    def unschedule_job(self, job_id: str):
        """Remove a job by ID"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Unscheduled job: {job_id}")
        except Exception as e:
            logger.error(f"Error unscheduling job {job_id}: {e}")

    def start(self):
        """Start the scheduler"""
        if not self.running:
            self.scheduler.start()
            self.running = True
            logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            logger.info("Scheduler stopped")

    def list_jobs(self) -> List[Dict]:
        """List all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time,
                    "trigger": str(job.trigger),
                }
            )
        return jobs

    def get_job_info(self, job_id: str) -> Optional[Dict]:
        """Get information about a specific job"""
        job = self.scheduler.get_job(job_id)
        if not job:
            return None

        return {
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time,
            "trigger": str(job.trigger),
        }
