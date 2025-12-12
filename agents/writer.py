from typing import Dict, Any


class WriterAgent:
    """
    Turns execution plan + messaging into concrete campaigns and posts.
    (Single-pass version to keep JSON stable.)
    """

    def __init__(self, llm):
        self.llm = llm

    def draft_and_review_assets(self, brief: Dict[str, Any], strategy: Dict[str, Any]) -> Dict[str, Any]:
        execution_plan = strategy.get("execution_plan")
        messaging = strategy.get("messaging_positioning")
        goals_kpis = brief.get("goals_kpis", "")
        target_audience = brief.get("target_audience", "")
        preferred_channels = brief.get("preferred_channels", "")

        prompt = f"""
You are a senior campaign designer and copywriter.

BRIEF:
{brief}

MESSAGING_POSITIONING:
{messaging}

EXECUTION_PLAN:
{execution_plan}

CONTEXT:
- Target audience: {target_audience}
- Goals & KPIs: {goals_kpis}
- Preferred channels: {preferred_channels}

TASK:
1) For this strategy, create 5–7 high-level campaigns. For each campaign, provide:
   - campaign_name
   - goal
   - key_message
   - main_channel
   - suggested_creative_idea

2) For each campaign, write 2 example posts with:
   - campaign_name
   - channel
   - copy (<= 120 words)
   - cta

All copy must:
- Align with the brief goals and audience.
- Use clear, non-clickbait language.

Return ONLY a single VALID JSON object with keys:
- "campaigns": list of campaign objects
- "posts": list of post objects
Do not include any other keys, comments, or text.
"""
        assets = self.llm(prompt)
        return assets
