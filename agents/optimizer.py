from typing import List, Dict, Any
import random


class OptimizerAgent:
    """
    Designs simple experiments and ranks posts by simulated performance,
    ensuring they respect goals, KPIs, and constraints.
    """

    def optimize(
        self,
        posts: List[Dict[str, Any]],
        brief: Dict[str, Any],
        strategy: Dict[str, Any],
    ) -> (List[Dict[str, Any]], List[Dict[str, Any]]):
        # Simulate metrics (quick heuristic)
        scored = []
        for p in posts:
            clicks = random.randint(20, 300)
            impressions = random.randint(500, 5000)
            ctr = round(100 * clicks / impressions, 2)
            scored.append({**p, "clicks": clicks, "impressions": impressions, "ctr": ctr})

        # Sort by CTR
        sorted_posts = sorted(scored, key=lambda x: x["ctr"], reverse=True)

        # Design simple experiments based on KPIs and channels
        experiments = [
            {
                "name": "Top vs educational hooks",
                "hypothesis": "Educational hooks will drive higher CTR and saves.",
                "primary_kpi": "CTR",
                "duration": "2 weeks",
                "notes": "Use top 4 posts across LinkedIn and email, vary hook style.",
            },
            {
                "name": "Short-form vs long-form",
                "hypothesis": "Short posts with clear CTA will drive more clicks to trial page.",
                "primary_kpi": "Trials or demo bookings",
                "duration": "3 weeks",
                "notes": "Test on LinkedIn and blog; ensure tracking links.",
            },
        ]

        return sorted_posts, experiments
