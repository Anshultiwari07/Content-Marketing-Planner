import ast
import streamlit as st
import pandas as pd

from main import run_campaign


st.set_page_config(
    page_title="CMP – Content Marketing Planner",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 CMP – Content Marketing Planner")
st.caption("World-class, brief-aware content marketing planner that thinks, checks, and optimizes.")


def as_list(value):
    """Normalize value to a list for clean bullet rendering."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    # try to parse "['a','b']" style strings
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
    return [value]


def safe_text(value) -> str:
    """Return a clean string for display or an empty string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value)


# ---------- Brief form ----------
with st.form("cmp_brief_form"):
    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input("Campaign topic", "AI tools for small businesses")
        product = st.text_input("Product / offer", "AI automation SaaS for SMEs")
        target_audience = st.text_area(
            "Target audience (who are we talking to?)",
            "Owners of small service businesses in US/Europe.",
            height=80,
        )
        preferred_channels = st.text_input(
            "Preferred channels",
            "LinkedIn, email, blog, YouTube shorts",
        )

    with col2:
        goals_kpis = st.text_area(
            "Goals & KPIs",
            "Increase trials by 30% in 3 months; KPIs: trials, demo bookings, CTR.",
            height=80,
        )
        budget = st.text_input(
            "Budget & resources",
            "Low to medium budget; mostly organic content and small paid tests.",
        )
        timeline_weeks = st.number_input(
            "Timeline (weeks)", min_value=2, max_value=12, value=6, step=1
        )
        constraints = st.text_area(
            "Constraints / must-nots",
            "No misleading claims; avoid heavy technical jargon; limited design team.",
            height=80,
        )

    additional_notes = st.text_area(
        "Additional notes (optional)",
        "",
        height=60,
    )

    submitted = st.form_submit_button("Generate CMP Plan ")


# ---------- Run CMP ----------
if submitted:
    brief = {
        "topic": topic,
        "product": product,
        "target_audience": target_audience,
        "goals_kpis": goals_kpis,
        "budget": budget,
        "preferred_channels": preferred_channels,
        "timeline_weeks": int(timeline_weeks),
        "constraints": constraints,
        "additional_notes": additional_notes,
    }

    with st.spinner("Thinking, validating, and planning your campaign..."):
        result = run_campaign(brief)

    strategy = result["strategy"]
    campaigns = result["campaigns"]
    posts = result["posts"]
    calendar = result["calendar"]
    experiments = result["experiments"]

    # ----- Brief summary -----
    st.markdown("###  Brief (what CMP understood)")
    st.markdown(
        f"""
**Topic:** {brief['topic']}  
**Product:** {brief['product']}  
**Audience:** {brief['target_audience']}  

**Goals & KPIs:** {brief['goals_kpis']}  
**Budget:** {brief['budget']}  
**Channels:** {brief['preferred_channels']}  
**Timeline:** {brief['timeline_weeks']} weeks  
**Constraints:** {brief['constraints']}
"""
    )

    # ----- Strategy sections -----
    st.markdown("###  Strategy ")
    col_left, col_right = st.columns(2, gap="large")

    # --- LEFT COLUMN ---
    with col_left:
        # Strategy overview
        with st.expander("Strategy overview", expanded=True):
            so = strategy.get("strategy_overview", {})
            summary = safe_text(so.get("summary"))
            if summary:
                st.markdown("**Summary**")
                st.write(summary)

            key_msgs = as_list(so.get("key_messages"))
            if key_msgs:
                st.markdown("**Key messages**")
                for m in key_msgs:
                    st.markdown(f"- {m}")

            chs = as_list(so.get("channels"))
            if chs:
                st.markdown("**Core channels**")
                st.markdown(", ".join(chs))

            vnotes = as_list(strategy.get("validation_notes"))
            if vnotes:
                st.markdown("**Validation notes**")
                for n in vnotes:
                    st.markdown(f"- {n}")

        # Target audience
        with st.expander("Target audience", expanded=False):
            ta = strategy.get("target_audience", {})
            seg = safe_text(ta.get("description") or ta.get("segment"))
            if seg:
                st.markdown(f"**Segment:** {seg}")
            loc = safe_text(ta.get("location"))
            if loc:
                st.markdown(f"**Location:** {loc}")

            pains = as_list(ta.get("pain_points") or ta.get("painpoints"))
            if pains:
                st.markdown("**Pain points**")
                for p in pains:
                    st.markdown(f"- {p}")

            interests = as_list(ta.get("interests"))
            if interests:
                st.markdown("**Interests**")
                for i in interests:
                    st.markdown(f"- {i}")

        # Market analysis
        with st.expander("Market analysis", expanded=False):
            ma = strategy.get("market_analysis", {})
            msize = safe_text(ma.get("market_size"))
            if msize:
                st.markdown(f"**Market size:** {msize}")
            trends = as_list(ma.get("market_trends"))
            if trends:
                st.markdown("**Trends**")
                for t in trends:
                    st.markdown(f"- {t}")
            comps = as_list(ma.get("competitor_analysis"))
            if comps:
                st.markdown("**Competitors**")
                for c in comps:
                    st.markdown(f"- {c}")
            insights = as_list(ma.get("market_insights"))
            if insights:
                st.markdown("**Insights**")
                for ins in insights:
                    st.markdown(f"- {ins}")

        # Customer journey
        with st.expander("Customer journey", expanded=False):
            cj = strategy.get("customer_journey", {})

            if isinstance(cj, list):
                for stage in cj:
                    if isinstance(stage, dict):
                        title = safe_text(stage.get("stage") or "Stage")
                        st.markdown(f"**{title}**")

                        desc = safe_text(stage.get("description"))
                        if desc:
                            st.write(desc)

                        kms = as_list(stage.get("key_messages"))
                        if kms:
                            for km in kms:
                                st.markdown(f"- {km}")
                    else:
                        st.markdown(f"- {stage}")

            elif isinstance(cj, dict):
                for stage_name, data in cj.items():
                    st.markdown(f"**{safe_text(stage_name)}**")

                    if isinstance(data, dict):
                        desc = safe_text(data.get("description"))
                        if desc:
                            st.write(desc)

                        kms = as_list(data.get("key_messages"))
                        if kms:
                            for km in kms:
                                st.markdown(f"- {km}")
                    else:
                        st.write(safe_text(data))

            else:
                st.info("No customer journey details provided in the strategy.")

    # --- RIGHT COLUMN ---
    with col_right:
        # Objectives & KPIs
        with st.expander("Objectives & KPIs", expanded=True):
            ok = strategy.get("objectives_kpis", {})
            has_content = False

            if isinstance(ok, dict):
                desc = safe_text(ok.get("description") or ok.get("objectives"))
                if desc:
                    has_content = True
                    st.markdown("**Objectives**")
                    st.write(desc)

                kpis = as_list(ok.get("kpis") or ok.get("kpi"))
                if kpis:
                    has_content = True
                    st.markdown("**KPIs**")
                    for k in kpis:
                        st.markdown(f"- {k}")

            elif isinstance(ok, list):
                if ok:
                    has_content = True
                    st.markdown("**Objectives & KPIs**")
                    for item in ok:
                        if isinstance(item, dict):
                            desc = safe_text(
                                item.get("description")
                                or item.get("objective")
                                or item.get("name")
                            )
                            if desc:
                                st.markdown(f"- {desc}")
                        else:
                            st.markdown(f"- {safe_text(item)}")

            if not has_content:
                st.info("No objectives & KPIs details provided in the strategy.")

        # Messaging & positioning
        with st.expander("Messaging & positioning", expanded=False):
            mp = strategy.get("messaging_positioning", {})
            msg = safe_text(mp.get("messaging") or mp.get("positioning_statement"))
            pos = safe_text(mp.get("positioning") or mp.get("unique_value_proposition"))
            kms = as_list(mp.get("key_messages"))

            has_content = False

            if msg:
                has_content = True
                st.markdown("**Messaging**")
                st.write(msg)

            if pos:
                has_content = True
                st.markdown("**Positioning**")
                st.write(pos)

            if kms:
                has_content = True
                st.markdown("**Key messages**")
                for km in kms:
                    st.markdown(f"- {km}")

            if not has_content:
                st.info("No messaging & positioning details provided in the strategy.")

        # Channel strategy
        with st.expander("Channel strategy", expanded=False):
            cs = strategy.get("channel_strategy", {})
            chs = cs.get("channels") if isinstance(cs, dict) else cs
            chs = as_list(chs)
            if chs:
                st.markdown("**Channels**")
                st.markdown(", ".join(chs))
            else:
                st.info("No channel strategy details provided in the strategy.")

        # Budget plan
        with st.expander("Budget plan", expanded=False):
            bp = strategy.get("budget_plan", {})

            total_budget = safe_text(bp.get("budget") or bp.get("total_budget"))
            notes = safe_text(bp.get("notes") or bp.get("description"))
            raw_alloc = bp.get("allocation") or bp.get("items") or bp.get("breakdown")
            alloc = as_list(raw_alloc)

            has_content = False

            if total_budget:
                has_content = True
                st.markdown(f"**Total budget:** {total_budget}")

            if notes:
                has_content = True
                st.markdown("**Notes**")
                st.write(notes)

            if alloc:
                has_content = True
                st.markdown("**Allocation**")
                for a in alloc:
                    if isinstance(a, dict):
                        label = (
                            a.get("category")
                            or a.get("channel")
                            or a.get("item")
                            or "Item"
                        )
                        amount = (
                            a.get("allocation")
                            or a.get("budget")
                            or a.get("cost")
                            or ""
                        )
                        extra = a.get("notes") or ""
                        line = f"- {label}"
                        if amount:
                            line += f": {amount}"
                        st.markdown(line)
                        if extra:
                            st.markdown(f"  - {extra}")
                    else:
                        st.markdown(f"- {a}")

            if not has_content:
                st.info("No budget details provided in the strategy.")

        # Trends & adaptation
        with st.expander("Trends & adaptation", expanded=False):
            tr = strategy.get("trend_adaptation", {})
            desc = safe_text(tr.get("strategy") or tr.get("description"))
            sources = as_list(tr.get("trend_sources"))

            if desc:
                st.write(desc)
            if sources:
                st.markdown("**Sources**")
                for s in sources:
                    st.markdown(f"- {s}")

            if not desc and not sources:
                st.info("No trends & adaptation details provided in the strategy.")

        # Analytics & feedback
        with st.expander("Analytics & feedback", expanded=False):
            af = strategy.get("analytics_feedback", {})

            if isinstance(af, str):
                text = safe_text(af)
                if text:
                    st.write(text)
                else:
                    st.info("No analytics details provided in the strategy.")
            else:
                desc = safe_text(af.get("description") or af.get("summary"))
                kpis = as_list(af.get("kpis") or af.get("metrics"))
                loops = as_list(af.get("feedback_loops") or af.get("processes"))
                tools = as_list(af.get("tools"))

                has_content = False

                if desc:
                    has_content = True
                    st.markdown("**Description**")
                    st.write(desc)

                if kpis:
                    has_content = True
                    st.markdown("**Kpis**")
                    for k in kpis:
                        st.markdown(f"- {k}")

                if loops:
                    has_content = True
                    st.markdown("**Feedback loops**")
                    for l in loops:
                        st.markdown(f"- {l}")

                if tools:
                    has_content = True
                    st.markdown("**Tools**")
                    for t in tools:
                        st.markdown(f"- {t}")

                if not has_content:
                    st.info("No analytics details provided in the strategy.")

    # ----- Execution calendar -----
    st.markdown("### 📅 Calendar (ready-to-implement schedule)")
    if calendar:
        cal_df = pd.DataFrame(calendar)
        cal_df.index = cal_df.index + 1  # start index at 1
        cols = [
            c
            for c in ["date", "campaign_name", "channel", "copy", "cta", "clicks", "impressions", "ctr"]
            if c in cal_df.columns
        ]
        st.dataframe(cal_df[cols], width="stretch", height=260)
    else:
        st.info("No calendar entries generated.")

    # ----- Campaigns & Posts side by side -----
    st.markdown("### Campaign assets")
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.subheader("🎯 Campaigns")
        if campaigns:
            camp_df = pd.DataFrame(campaigns)
            camp_df.index = camp_df.index + 1  # start index at 1
            st.dataframe(camp_df, width="stretch", height=260)
        else:
            st.info("No campaigns generated yet.")

    with c2:
        st.subheader("✍️ Posts (top-ranked)")
        if posts:
            posts_df = pd.DataFrame(posts)
            posts_df.index = posts_df.index + 1  # start index at 1
            cols = [
                c
                for c in ["campaign_name", "channel", "copy", "cta", "clicks", "impressions", "ctr"]
                if c in posts_df.columns
            ]
            st.dataframe(posts_df[cols], width="stretch", height=260)
        else:
            st.info("No posts generated yet.")

    # ----- Experiments -----
    st.markdown("### 🧪 Experiments & Testing Plan")
    if experiments:
        exp_df = pd.DataFrame(experiments)
        exp_df.index = exp_df.index + 1  # start index at 1
        st.dataframe(exp_df, width="stretch", height=220)
    else:
        st.info("No experiments defined yet.")
