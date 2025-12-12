from typing import Dict, Any


class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def plan_strategy_and_campaign(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        weeks = brief.get("timeline_weeks", 6)

        prompt = f"""
You are CMP, the world's best content marketing planner.

BRIEF (JSON):
{brief}

TASK:
Create a FULL strategy object with EXACTLY these top-level keys:
- "strategy_overview"
- "target_audience"
- "market_analysis"
- "customer_journey"
- "objectives_kpis"
- "messaging_positioning"
- "channel_strategy"
- "budget_plan"
- "trend_adaptation"
- "analytics_feedback"
- "execution_plan"

Requirements:
- "strategy_overview": summary, key_messages, channels.
- "execution_plan": a LIST of weeks. Each week is an OBJECT with:
  - week_number
  - theme
  - main_objective
  - key_message
  - channels (list of strings)
  - campaign_ideas (list of strings)

Return ONLY a single VALID JSON object with those keys.
No explanations, no extra fields.
"""
        strategy = self.llm(prompt)
        return strategy
