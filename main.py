import os
import json
from datetime import date

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from agents import PlannerAgent, ResearcherAgent, WriterAgent, OptimizerAgent
from tools import TavilySearchTool, CalendarTool, MetricsSimulator

load_dotenv()


def extract_json(text: str):
    """
    Extract the FIRST complete {...} block from the model output and parse it.

    - If the whole text is valid JSON, parse it directly.
    - Otherwise, find the first balanced {...} block and parse that.
    - If no balanced block exists, raise ValueError.
    """
    if not text:
        raise ValueError("Model output is empty.")

    text = text.strip()

    # Fast path: entire output is valid JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Fallback: find first '{' and walk to matching '}'
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object start found in model output:\n{text}")

    depth = 0
    end = None
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1  # include this closing brace
                break

    if end is None:
        raise ValueError(f"No complete JSON object found in model output:\n{text}")

    json_str = text[start:end]
    try:
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Could not parse JSON candidate:\n{json_str}\nError: {e}")


def make_llm():
    hf_token = os.getenv("HF_API_KEY")
    model_id = os.getenv("HF_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct")

    client = InferenceClient(model=model_id, token=hf_token)

    def call_llm(prompt: str):
        response = client.chat_completion(
            model=model_id,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior marketing AI that ONLY responds with a "
                        "single valid JSON object. No prose, no markdown, no bullet "
                        "lists outside JSON, and no explanations.\n\n"
                        "The JSON must:\n"
                        "- Start with '{' and end with '}'.\n"
                        "- Be valid so that json.loads() succeeds.\n"
                        "- Contain keys like strategy_overview, target_audience, "
                        "market_analysis, customer_journey, objectives_kpis, "
                        "messaging_positioning, channel_strategy, budget_plan, "
                        "trend_adaptation, analytics_feedback, campaigns, posts, etc., "
                        "depending on the prompt.\n"
                        "- NOT include any extremely long week-by-week execution_plan "
                        "or verbose schedules; keep fields concise so the JSON fits "
                        "within the token limit."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1400,
            temperature=0.4,
        )
        text = response.choices[0].message["content"]
        return extract_json(text)

    return call_llm


def run_campaign(brief: dict):
    """
    brief = {
        'topic': str,
        'product': str,
        'target_audience': str,
        'goals_kpis': str,
        'budget': str,
        'preferred_channels': str,
        'timeline_weeks': int,
        'constraints': str,
        'additional_notes': str,
    }
    """
    llm = make_llm()

    planner = PlannerAgent(llm)
    researcher = ResearcherAgent(llm, TavilySearchTool())
    writer = WriterAgent(llm)
    optimizer = OptimizerAgent()
    calendar_tool = CalendarTool()
    metrics_sim = MetricsSimulator()

    # 1) Strategy v2 (two-pass planner, using full brief)
    strategy = planner.plan_strategy_and_campaign(brief)

    # 2) Validate market & trends with web + add validation_notes
    strategy = researcher.enrich_and_validate_strategy(brief, strategy)

    # 3) Draft campaigns + posts with review pass
    assets = writer.draft_and_review_assets(brief, strategy)
    campaigns = assets.get("campaigns", [])
    posts = assets.get("posts", [])

    # 4) Simulate metrics + design experiments + pick winners
    scored_posts = metrics_sim.simulate(posts)
    best_posts, experiments = optimizer.optimize(scored_posts, brief, strategy)

    # 5) Build calendar
    calendar = calendar_tool.build_calendar(best_posts, start_date=date.today())

    return {
        "brief": brief,
        "strategy": strategy,
        "campaigns": campaigns,
        "posts": best_posts,
        "experiments": experiments,
        "calendar": calendar,
    }


if __name__ == "__main__":
    sample_brief = {
        "topic": "AI tools for small businesses",
        "product": "SaaS platform that bundles AI automations for SMEs",
        "target_audience": "Owners of small service businesses in US/Europe",
        "goals_kpis": "Increase product trials by 30% in 3 months; primary KPIs: trials, demo bookings, CTR",
        "budget": "Low to medium budget, mostly organic + small paid tests",
        "preferred_channels": "LinkedIn, email, blog, YouTube shorts",
        "timeline_weeks": 6,
        "constraints": "No big brand ads; avoid over-technical jargon",
        "additional_notes": "",
    }
    result = run_campaign(sample_brief)
    print("TOP-LEVEL KEYS:", result.keys())
    print("Strategy keys:", result["strategy"].keys())
    print("# campaigns:", len(result["campaigns"]))
    print("# posts:", len(result["posts"]))
    print("# calendar entries:", len(result["calendar"]))
