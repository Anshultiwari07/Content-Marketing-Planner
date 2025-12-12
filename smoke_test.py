from main import run_campaign

def main():
    brief = {
        "topic": "AI tools for small businesses",
        "product": "AI automation SaaS for SMEs",
        "target_audience": "Owners of small service businesses in US/Europe",
        "goals_kpis": "Increase trials by 30% in 3 months; KPIs: trials, demo bookings, CTR",
        "budget": "Low–medium budget; mostly organic + small paid tests",
        "preferred_channels": "LinkedIn, email, blog, YouTube shorts",
        "timeline_weeks": 6,
        "constraints": "No misleading claims; avoid heavy jargon",
        "additional_notes": "",
    }
    result = run_campaign(brief)
    print("TOP-LEVEL KEYS:", result.keys())

if __name__ == "__main__":
    main()
 