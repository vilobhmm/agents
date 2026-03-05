"""
Prioritization Engine — Multiple frameworks for feature/initiative prioritization.

Frameworks: RICE, ICE, MoSCoW, Kano Model, Opportunity Scoring, Stack Ranking.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Feature:
    """A feature or initiative to be prioritized."""
    name: str
    description: str = ""
    reach: int = 0        # RICE: users impacted per quarter
    impact: int = 0       # 1-3 scale (minimal, medium, massive)
    confidence: int = 0   # 0-100%
    effort: int = 0       # person-weeks


class PMPrioritization:
    """
    Multi-framework prioritization engine.

    Supports RICE, ICE, MoSCoW, Kano Model, and custom frameworks.
    All methods are deterministic (no API calls needed).
    """

    # ── RICE Score ───────────────────────────────────────────────

    def rice_score(
        self,
        features: List[Dict],
    ) -> List[Dict]:
        """
        Calculate RICE scores and rank features.

        Args:
            features: List of dicts with keys:
                - name (str), reach (int), impact (1-3), confidence (0-100), effort (int)

        Returns:
            Ranked list with RICE scores

        Example:
            >>> engine.rice_score([
            ...     {"name": "Search", "reach": 5000, "impact": 3, "confidence": 80, "effort": 4},
            ...     {"name": "Export", "reach": 1000, "impact": 1, "confidence": 90, "effort": 2},
            ... ])
        """
        scored = []
        for f in features:
            reach = f.get("reach", 0)
            impact = f.get("impact", 1)
            confidence = f.get("confidence", 50) / 100
            effort = max(f.get("effort", 1), 1)

            # RICE = (Reach × Impact × Confidence) / Effort
            rice = (reach * impact * confidence) / effort

            scored.append({
                **f,
                "rice_score": round(rice, 1),
                "formula": f"({reach} × {impact} × {confidence:.0%}) / {effort}",
            })

        scored.sort(key=lambda x: x["rice_score"], reverse=True)

        # Add rank
        for i, item in enumerate(scored, 1):
            item["rank"] = i

        return scored

    # ── ICE Score ────────────────────────────────────────────────

    def ice_score(
        self,
        features: List[Dict],
    ) -> List[Dict]:
        """
        Calculate ICE scores (Impact × Confidence × Ease).

        Args:
            features: List of dicts with keys:
                - name (str), impact (1-10), confidence (1-10), ease (1-10)

        Returns:
            Ranked list with ICE scores
        """
        scored = []
        for f in features:
            impact = f.get("impact", 5)
            confidence = f.get("confidence", 5)
            ease = f.get("ease", 5)

            ice = impact * confidence * ease

            scored.append({
                **f,
                "ice_score": ice,
                "formula": f"{impact} × {confidence} × {ease}",
            })

        scored.sort(key=lambda x: x["ice_score"], reverse=True)
        for i, item in enumerate(scored, 1):
            item["rank"] = i

        return scored

    # ── MoSCoW ──────────────────────────────────────────────────

    def moscow_classify(
        self,
        features: List[Dict],
    ) -> Dict[str, List[Dict]]:
        """
        Classify features using MoSCoW framework.

        Args:
            features: List of dicts with keys:
                - name (str), category (str: "must", "should", "could", "wont")
                - Optional: reason (str)

        Returns:
            Features grouped by MoSCoW category
        """
        result = {
            "must_have": [],
            "should_have": [],
            "could_have": [],
            "wont_have": [],
        }

        category_map = {
            "must": "must_have",
            "should": "should_have",
            "could": "could_have",
            "wont": "wont_have",
            "won't": "wont_have",
        }

        for f in features:
            category = f.get("category", "could").lower()
            bucket = category_map.get(category, "could_have")
            result[bucket].append({
                "name": f.get("name", ""),
                "description": f.get("description", ""),
                "reason": f.get("reason", ""),
            })

        # Add summary
        total = len(features)
        result["summary"] = {
            "total": total,
            "must_have_count": len(result["must_have"]),
            "should_have_count": len(result["should_have"]),
            "could_have_count": len(result["could_have"]),
            "wont_have_count": len(result["wont_have"]),
            "must_have_pct": round(len(result["must_have"]) / max(total, 1) * 100),
        }

        return result

    # ── Kano Model ──────────────────────────────────────────────

    def kano_classify(
        self,
        features: List[Dict],
    ) -> Dict[str, List[Dict]]:
        """
        Classify features using the Kano Model.

        Args:
            features: List of dicts with keys:
                - name (str)
                - functional (str): reaction when feature is present
                  ("like", "expect", "neutral", "tolerate", "dislike")
                - dysfunctional (str): reaction when feature is absent
                  ("like", "expect", "neutral", "tolerate", "dislike")

        Returns:
            Features classified as: must_be, performance, attractive, indifferent, reverse
        """
        # Kano evaluation table
        kano_table = {
            ("like", "dislike"): "attractive",
            ("like", "tolerate"): "attractive",
            ("like", "neutral"): "attractive",
            ("like", "expect"): "performance",
            ("expect", "dislike"): "must_be",
            ("expect", "tolerate"): "must_be",
            ("expect", "neutral"): "indifferent",
            ("neutral", "dislike"): "must_be",
            ("neutral", "neutral"): "indifferent",
            ("dislike", "like"): "reverse",
            ("tolerate", "like"): "reverse",
        }

        result = {
            "must_be": [],
            "performance": [],
            "attractive": [],
            "indifferent": [],
            "reverse": [],
        }

        for f in features:
            func = f.get("functional", "neutral").lower()
            dysfunc = f.get("dysfunctional", "neutral").lower()
            category = kano_table.get((func, dysfunc), "indifferent")

            result[category].append({
                "name": f.get("name", ""),
                "functional": func,
                "dysfunctional": dysfunc,
            })

        return result

    # ── Opportunity Scoring ─────────────────────────────────────

    def opportunity_score(
        self,
        features: List[Dict],
    ) -> List[Dict]:
        """
        Calculate Opportunity Scores (Outcome-Driven Innovation).

        Formula: Opportunity = Importance + max(Importance - Satisfaction, 0)

        Args:
            features: List of dicts with keys:
                - name (str), importance (1-10), satisfaction (1-10)

        Returns:
            Ranked list with opportunity scores
        """
        scored = []
        for f in features:
            importance = f.get("importance", 5)
            satisfaction = f.get("satisfaction", 5)

            # ODI formula
            gap = max(importance - satisfaction, 0)
            opportunity = importance + gap

            scored.append({
                **f,
                "opportunity_score": round(opportunity, 1),
                "gap": gap,
                "classification": (
                    "over-served" if satisfaction > importance
                    else "appropriately-served" if gap < 2
                    else "under-served"
                ),
            })

        scored.sort(key=lambda x: x["opportunity_score"], reverse=True)
        for i, item in enumerate(scored, 1):
            item["rank"] = i

        return scored

    # ── Stack Ranking ───────────────────────────────────────────

    def stack_rank(
        self,
        features: List[Dict],
        weights: Optional[Dict[str, float]] = None,
    ) -> List[Dict]:
        """
        Stack rank features using weighted multi-criteria scoring.

        Args:
            features: List of dicts with keys:
                - name (str), plus any numeric scoring dimensions
            weights: Optional dimension -> weight mapping.
                Defaults to equal weights across all numeric dimensions.

        Returns:
            Ranked list with weighted scores
        """
        if not features:
            return []

        # Identify numeric dimensions (exclude 'name', 'description', etc.)
        skip_keys = {"name", "description", "reason", "category"}
        sample = features[0]
        dimensions = [k for k in sample if k not in skip_keys and isinstance(sample.get(k), (int, float))]

        if not dimensions:
            return [{"name": f.get("name", ""), "rank": i + 1} for i, f in enumerate(features)]

        if weights is None:
            weights = {d: 1.0 / len(dimensions) for d in dimensions}

        scored = []
        for f in features:
            weighted_score = sum(
                f.get(dim, 0) * weights.get(dim, 0)
                for dim in dimensions
            )
            scored.append({
                **f,
                "weighted_score": round(weighted_score, 2),
            })

        scored.sort(key=lambda x: x["weighted_score"], reverse=True)
        for i, item in enumerate(scored, 1):
            item["rank"] = i

        return scored
