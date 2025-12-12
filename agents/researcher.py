from typing import Dict, Any
from tools.tavily_search import TavilySearchTool


class ResearcherAgent:
    """
    Uses web search to validate and deepen market_analysis and trend_adaptation.
    Adds validation_notes to make CMP transparent about confidence.
    """

    def __init__(self, llm, search_tool: TavilySearchTool):
        self.llm = llm
        self.search_tool = search_tool

    def enrich_and_validate_strategy(
        self, brief: Dict[str, Any], strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        topic = brief.get("topic")
        snippets = self.search_tool.search(
            f"{topic} latest industry trends, competitors, positioning, audience"
        )

        prompt = f"""
You are a marketing research validator.

BRIEF:
{brief}

CURRENT_STRATEGY:
market_analysis: {strategy.get('market_analysis')}
trend_adaptation: {strategy.get('trend_adaptation')}

WEB_SNIPPETS:
{snippets}

TASK:
1) Refine and deepen ONLY "market_analysis" and "trend_adaptation" using the snippets.
2) Add "validation_notes" as a list of short bullet-point strings describing
   risks, contradictions, or uncertainties (focus on market & trends).

Return ONLY a single VALID JSON object with EXACT keys:
["market_analysis","trend_adaptation","validation_notes"].
Do not include any other keys, text, or comments.
"""
        updated = self.llm(prompt)

        strategy["market_analysis"] = updated.get(
            "market_analysis", strategy.get("market_analysis")
        )
        strategy["trend_adaptation"] = updated.get(
            "trend_adaptation", strategy.get("trend_adaptation")
        )
        strategy["validation_notes"] = updated.get("validation_notes", [])
        return strategy
