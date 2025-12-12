from typing import List, Dict
import random

class MetricsSimulator:
    def simulate(self, posts: List[Dict]) -> List[Dict]:
        enriched = []
        for p in posts:
            clicks = random.randint(20, 300)
            impressions = random.randint(500, 5000)
            ctr = round(100 * clicks / impressions, 2)
            enriched.append({**p, "clicks": clicks, "impressions": impressions, "ctr": ctr})
        return enriched
