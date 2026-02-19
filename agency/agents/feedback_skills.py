"""
Feedback Management Skills - Executable commands for feedback lifecycle.

Provides direct skill commands for:
- Clustering feedback by theme
- Enriching with logs and root cause
- Tracking bugs and updates
- Generating solutions with PRDs
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackSkills:
    """
    Skills for Feedback Management team.

    Executable commands that can be invoked via:
    - /cluster-feedback
    - /enrich-feedback
    - /track-bugs
    - /generate-solutions
    - /feedback-report
    """

    def __init__(self):
        """Initialize with feedback tools"""
        try:
            from agency.tools.feedback_tools import (
                get_feedback_reports,
                create_cluster,
                enrich_feedback,
                create_bug,
                post_bug_update,
                create_solution,
                get_feedback_analytics,
                get_clusters,
                get_bugs,
                get_solutions,
            )
            self.get_feedback_reports = get_feedback_reports
            self.create_cluster = create_cluster
            self.enrich_feedback = enrich_feedback
            self.create_bug = create_bug
            self.post_bug_update = post_bug_update
            self.create_solution = create_solution
            self.get_feedback_analytics = get_feedback_analytics
            self.get_clusters = get_clusters
            self.get_bugs = get_bugs
            self.get_solutions = get_solutions
            self.enabled = True
        except ImportError as e:
            logger.warning(f"Feedback tools not available: {e}")
            self.enabled = False

    async def cluster_feedback(
        self,
        status: str = "new",
        min_cluster_size: int = 2
    ) -> Dict:
        """
        Cluster recent feedback into themes.

        Analyzes all feedback with given status, groups by similarity,
        and creates clusters with themes and root causes.

        Args:
            status: Feedback status to cluster (default: "new")
            min_cluster_size: Minimum feedback items per cluster

        Returns:
            Dict with clusters created and statistics
        """
        logger.info(f"Clustering feedback with status: {status}")

        if not self.enabled:
            return {"error": "Feedback tools not available"}

        try:
            # Get feedback to cluster
            feedback = self.get_feedback_reports(status=status)

            if len(feedback) < min_cluster_size:
                return {
                    "status": "insufficient_data",
                    "message": f"Only {len(feedback)} feedback items. Need at least {min_cluster_size} to cluster.",
                    "feedback_count": len(feedback)
                }

            # In a real implementation, this would use NLP/embeddings
            # For now, we'll demonstrate the structure
            clusters_created = []

            # Example: Group by keyword similarity (simplified)
            themes = self._identify_themes(feedback)

            for theme, items in themes.items():
                if len(items) >= min_cluster_size:
                    cluster = self.create_cluster(
                        theme=theme,
                        description=f"Cluster of {len(items)} feedback items related to {theme}",
                        feedback_ids=[item['id'] for item in items],
                        root_cause=self._analyze_root_cause(items)
                    )
                    clusters_created.append(cluster)

            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "total_feedback": len(feedback),
                "clusters_created": len(clusters_created),
                "clusters": clusters_created,
                "message": f"Created {len(clusters_created)} clusters from {len(feedback)} feedback items"
            }

        except Exception as e:
            logger.error(f"Error clustering feedback: {e}")
            return {"status": "error", "error": str(e)}

    async def enrich_feedback_batch(
        self,
        feedback_ids: Optional[List[str]] = None,
        auto_analyze: bool = True
    ) -> Dict:
        """
        Enrich feedback with logs and root cause analysis.

        Args:
            feedback_ids: Specific feedback IDs to enrich (None = all new)
            auto_analyze: Automatically analyze logs for root cause

        Returns:
            Dict with enrichment results
        """
        logger.info("Enriching feedback with logs and context")

        if not self.enabled:
            return {"error": "Feedback tools not available"}

        try:
            # Get feedback to enrich
            if feedback_ids:
                # Get specific feedback
                all_feedback = self.get_feedback_reports()
                feedback = [f for f in all_feedback if f['id'] in feedback_ids]
            else:
                # Get all clustered feedback
                feedback = self.get_feedback_reports(status="clustered")

            enriched = []

            for item in feedback:
                user_id = item.get('user_id', 'unknown')

                # Simulate log analysis (in production, would actually fetch and analyze logs)
                enrichment_data = {
                    "logs": f"Simulated logs for {user_id}",
                    "conversation_history": f"User reported issue on {item.get('created_at', 'unknown date')}",
                    "reproduction_steps": self._extract_reproduction_steps(item),
                }

                if auto_analyze:
                    enrichment_data["root_cause"] = self._analyze_root_cause([item])

                self.enrich_feedback(
                    feedback_id=item['id'],
                    **enrichment_data
                )
                enriched.append(item['id'])

            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "enriched_count": len(enriched),
                "feedback_ids": enriched,
                "message": f"Enriched {len(enriched)} feedback items with logs and root cause"
            }

        except Exception as e:
            logger.error(f"Error enriching feedback: {e}")
            return {"status": "error", "error": str(e)}

    async def track_bugs(
        self,
        auto_create: bool = True,
        min_feedback_per_bug: int = 2
    ) -> Dict:
        """
        Track bugs from clustered feedback.

        Creates bugs from clusters and posts updates when new
        related feedback arrives.

        Args:
            auto_create: Automatically create bugs from clusters
            min_feedback_per_bug: Minimum feedback items to create bug

        Returns:
            Dict with bug tracking results
        """
        logger.info("Tracking bugs from feedback clusters")

        if not self.enabled:
            return {"error": "Feedback tools not available"}

        try:
            clusters = self.get_clusters(status="active")
            existing_bugs = self.get_bugs(status="open")

            bugs_created = []
            bugs_updated = []

            for cluster in clusters:
                feedback_count = len(cluster.get('feedback_ids', []))

                if feedback_count < min_feedback_per_bug:
                    continue

                # Check if bug already exists for this cluster
                existing_bug = next(
                    (b for b in existing_bugs if b.get('cluster_id') == cluster['id']),
                    None
                )

                if existing_bug:
                    # Update existing bug
                    new_feedback = [
                        fid for fid in cluster['feedback_ids']
                        if fid not in existing_bug.get('feedback_ids', [])
                    ]

                    if new_feedback:
                        self.post_bug_update(
                            bug_id=existing_bug['id'],
                            update_text=f"Received {len(new_feedback)} new related feedback reports. Total: {len(cluster['feedback_ids'])}",
                            new_feedback_ids=new_feedback
                        )
                        bugs_updated.append(existing_bug['id'])

                elif auto_create:
                    # Create new bug
                    severity = self._calculate_severity(cluster)

                    bug = self.create_bug(
                        title=f"{cluster['theme']} - {feedback_count} reports",
                        description=cluster['description'],
                        severity=severity,
                        cluster_id=cluster['id'],
                        feedback_ids=cluster['feedback_ids']
                    )
                    bugs_created.append(bug['id'])

            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "clusters_analyzed": len(clusters),
                "bugs_created": len(bugs_created),
                "bugs_updated": len(bugs_updated),
                "created_bug_ids": bugs_created,
                "updated_bug_ids": bugs_updated,
                "message": f"Created {len(bugs_created)} bugs, updated {len(bugs_updated)} bugs"
            }

        except Exception as e:
            logger.error(f"Error tracking bugs: {e}")
            return {"status": "error", "error": str(e)}

    async def generate_solutions(
        self,
        bug_ids: Optional[List[str]] = None,
        include_prd: bool = True,
        include_prototype: bool = False,
        include_coding_prompt: bool = True
    ) -> Dict:
        """
        Generate solutions for bugs.

        Creates PRDs, prototypes, and coding agent prompts
        for each bug.

        Args:
            bug_ids: Specific bug IDs (None = all open bugs)
            include_prd: Generate Product Requirement Document
            include_prototype: Generate prototype description
            include_coding_prompt: Generate coding agent prompt

        Returns:
            Dict with generated solutions
        """
        logger.info("Generating solutions for bugs")

        if not self.enabled:
            return {"error": "Feedback tools not available"}

        try:
            # Get bugs to solve
            if bug_ids:
                all_bugs = self.get_bugs()
                bugs = [b for b in all_bugs if b['id'] in bug_ids]
            else:
                bugs = self.get_bugs(status="open")

            solutions_created = []

            for bug in bugs:
                # Check if solution already exists
                existing = self.get_solutions(bug_id=bug['id'])
                if existing:
                    continue

                # Generate solution components
                prd = None
                if include_prd:
                    prd = self._generate_prd(bug)

                prototype = None
                if include_prototype:
                    prototype = self._generate_prototype(bug)

                coding_prompt = None
                if include_coding_prompt:
                    coding_prompt = self._generate_coding_prompt(bug)

                solution = self.create_solution(
                    bug_id=bug['id'],
                    title=f"Solution for: {bug['title']}",
                    approach=self._generate_approach(bug),
                    prd=prd,
                    prototype=prototype,
                    coding_prompt=coding_prompt,
                    trade_offs=self._analyze_tradeoffs(bug),
                    effort_estimate=self._estimate_effort(bug)
                )

                solutions_created.append(solution['id'])

            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "bugs_analyzed": len(bugs),
                "solutions_created": len(solutions_created),
                "solution_ids": solutions_created,
                "components": {
                    "prd": include_prd,
                    "prototype": include_prototype,
                    "coding_prompt": include_coding_prompt
                },
                "message": f"Generated {len(solutions_created)} solutions for {len(bugs)} bugs"
            }

        except Exception as e:
            logger.error(f"Error generating solutions: {e}")
            return {"status": "error", "error": str(e)}

    async def feedback_report(
        self,
        include_trends: bool = True,
        include_top_issues: bool = True,
        top_n: int = 5
    ) -> Dict:
        """
        Generate comprehensive feedback analytics report.

        Args:
            include_trends: Include trend analysis
            include_top_issues: Include top issues by feedback count
            top_n: Number of top issues to include

        Returns:
            Dict with analytics report
        """
        logger.info("Generating feedback analytics report")

        if not self.enabled:
            return {"error": "Feedback tools not available"}

        try:
            analytics = self.get_feedback_analytics()
            clusters = self.get_clusters()
            bugs = self.get_bugs()
            solutions = self.get_solutions()

            report = {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "analytics": analytics,
                "summary": {
                    "total_feedback": analytics['total_feedback'],
                    "active_clusters": len([c for c in clusters if c.get('status') == 'active']),
                    "open_bugs": analytics['bugs_by_status'].get('open', 0),
                    "proposed_solutions": analytics['solutions_by_status'].get('proposed', 0)
                }
            }

            if include_top_issues:
                # Get clusters sorted by feedback count
                top_clusters = sorted(
                    clusters,
                    key=lambda c: len(c.get('feedback_ids', [])),
                    reverse=True
                )[:top_n]

                report["top_issues"] = [
                    {
                        "theme": c['theme'],
                        "feedback_count": len(c.get('feedback_ids', [])),
                        "description": c.get('description', '')[:100]
                    }
                    for c in top_clusters
                ]

            if include_trends:
                # Simple trend analysis
                report["trends"] = {
                    "new_feedback_rate": "Simulated: 5 per day",
                    "resolution_rate": "Simulated: 3 per day",
                    "average_time_to_cluster": "Simulated: 2 hours"
                }

            return report

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {"status": "error", "error": str(e)}

    # ─── Helper Methods ───────────────────────────────────────────────────

    def _identify_themes(self, feedback: List[Dict]) -> Dict[str, List[Dict]]:
        """Group feedback by common themes (simplified)"""
        themes = {}

        for item in feedback:
            text = item.get('feedback_text', '').lower()

            # Simple keyword-based grouping
            if 'slow' in text or 'performance' in text or 'load' in text:
                themes.setdefault('Performance Issues', []).append(item)
            elif 'crash' in text or 'error' in text or 'bug' in text:
                themes.setdefault('Crashes and Errors', []).append(item)
            elif 'ui' in text or 'design' in text or 'layout' in text:
                themes.setdefault('UI/UX Issues', []).append(item)
            else:
                themes.setdefault('Other Issues', []).append(item)

        return themes

    def _analyze_root_cause(self, feedback: List[Dict]) -> str:
        """Analyze root cause from feedback items"""
        # In production, would use LLM to analyze
        return f"Potential root cause based on {len(feedback)} feedback items (simulated analysis)"

    def _extract_reproduction_steps(self, feedback: Dict) -> List[str]:
        """Extract reproduction steps from feedback"""
        return [
            "1. Reproduce the issue described in feedback",
            "2. Check system logs for errors",
            "3. Verify user environment matches reported conditions"
        ]

    def _calculate_severity(self, cluster: Dict) -> str:
        """Calculate bug severity from cluster"""
        feedback_count = len(cluster.get('feedback_ids', []))

        if feedback_count >= 10:
            return "critical"
        elif feedback_count >= 5:
            return "high"
        elif feedback_count >= 2:
            return "medium"
        else:
            return "low"

    def _generate_prd(self, bug: Dict) -> str:
        """Generate Product Requirement Document"""
        return f"""# PRD: {bug['title']}

## Problem
{bug['description']}

## Solution Approach
[Detailed solution approach would be generated here]

## Success Metrics
- Bug resolved
- No new related reports for 2 weeks
- User satisfaction improved

## Timeline
- Week 1: Investigation and design
- Week 2: Implementation
- Week 3: Testing and rollout

## Resources Required
- 1 engineer
- QA support
- Design review (if UI changes)
"""

    def _generate_prototype(self, bug: Dict) -> str:
        """Generate prototype description"""
        return f"Prototype link: [Figma/Design tool] for {bug['title']}"

    def _generate_coding_prompt(self, bug: Dict) -> str:
        """Generate coding agent prompt"""
        return f"""You are a senior engineer fixing this bug:

Bug: {bug['title']}
Description: {bug['description']}
Severity: {bug['severity']}

Tasks:
1. Identify root cause in the codebase
2. Implement fix with minimal changes
3. Add unit tests to prevent regression
4. Update documentation if needed
5. Create pull request with clear description

Follow best practices:
- Write clean, maintainable code
- Add comprehensive tests
- Update CHANGELOG
- Consider edge cases
"""

    def _generate_approach(self, bug: Dict) -> str:
        """Generate solution approach"""
        return f"Address {bug['title']} by implementing targeted fix with comprehensive testing"

    def _analyze_tradeoffs(self, bug: Dict) -> str:
        """Analyze solution trade-offs"""
        return """
**Pros:**
- Directly addresses reported issue
- Minimal code changes
- Low risk

**Cons:**
- May require testing across environments
- Potential for edge cases

**Alternatives:**
- Quick patch vs. comprehensive refactor (evaluate based on severity)
"""

    def _estimate_effort(self, bug: Dict) -> str:
        """Estimate effort"""
        severity = bug.get('severity', 'medium')

        if severity == 'critical':
            return "1-2 days (urgent)"
        elif severity == 'high':
            return "3-5 days"
        elif severity == 'medium':
            return "1 week"
        else:
            return "1-2 weeks (low priority)"
