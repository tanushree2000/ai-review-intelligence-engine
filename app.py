import streamlit as st
import pandas as pd
import ast
import os

st.set_page_config(
    page_title="VoC Intelligence Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

section[data-testid="stSidebar"] {
    background: #1a1a2e;
    border-right: 1px solid #2e2e4e;
}
section[data-testid="stSidebar"] * { color: #c8c8e0 !important; }
section[data-testid="stSidebar"] .sidebar-title {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff !important;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid #2e2e4e;
    margin-bottom: 1rem;
}
section[data-testid="stSidebar"] .sidebar-nav-item {
    display: block;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    margin-bottom: 4px;
    transition: background .15s;
}
section[data-testid="stSidebar"] .sidebar-nav-item:hover { background: #2e2e4e; }
section[data-testid="stSidebar"] .sidebar-nav-item.active {
    background: #e8634a;
    color: #fff !important;
}
section[data-testid="stSidebar"] .sidebar-section {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #666 !important;
    margin: 1.2rem 0 .4rem;
}
section[data-testid="stSidebar"] .sidebar-stat {
    background: #12122a;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 13px;
}
section[data-testid="stSidebar"] .sidebar-stat-val {
    font-size: 20px;
    font-weight: 700;
    color: #fff !important;
}

.page-title {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0;
}
.breadcrumb {
    font-size: 12px;
    color: #999;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #fff;
    border: 1px solid #eee;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
}
.metric-card-dark {
    background: #1a1a2e;
    border: none;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #999;
    margin-bottom: 6px;
}
.metric-label-dark {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #666;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1;
}
.metric-value-dark {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.metric-trend-pos {
    font-size: 12px;
    color: #4caf82;
    font-weight: 500;
    margin-top: 6px;
}
.metric-trend-neg {
    font-size: 12px;
    color: #e57373;
    font-weight: 500;
    margin-top: 6px;
}
.metric-icon {
    position: absolute;
    top: 1.2rem;
    right: 1.4rem;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.chart-card {
    background: #fff;
    border: 1px solid #eee;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
}
.chart-card-dark {
    background: #1a1a2e;
    border: none;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
}
.chart-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #999;
    margin-bottom: 1rem;
}
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
}
.pos { background: #e8f5ee; color: #2e7d52; }
.neg { background: #fdecea; color: #c62828; }
.p0  { background: #fdecea; color: #c62828; }
.p1  { background: #fff8e1; color: #f57f17; }
.p2  { background: #e8f5ee; color: #2e7d52; }
.eng { background: #e3f2fd; color: #1565c0; }
.prd { background: #f3e5f5; color: #6a1b9a; }
.des { background: #fce4ec; color: #880e4f; }
.action-row {
    background: #fafafa;
    border: 1px solid #f0f0f0;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-size: 13px;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;
}
.pain-row {
    border-left: 3px solid #e57373;
    background: #fff8f8;
    border-radius: 0 8px 8px 0;
    padding: 8px 12px;
    margin: 5px 0;
    font-size: 13px;
    color: #444;
}
.delight-row {
    border-left: 3px solid #4caf82;
    background: #f8fff9;
    border-radius: 0 8px 8px 0;
    padding: 8px 12px;
    margin: 5px 0;
    font-size: 13px;
    color: #444;
}
.summary-row {
    background: #fafafa;
    border: 1px solid #f0f0f0;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-size: 13px;
    color: #444;
}
.divider { border-top: 1px solid #f0f0f0; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    for p in [
        os.path.join(base, "outputs", "review_intel_outputs.csv"),
        os.path.join(base, "review_intel_outputs.csv"),
    ]:
        if os.path.exists(p):
            df = pd.read_csv(p)
            def safe_parse(val):
                try: return ast.literal_eval(val)
                except: return []
            for col in ["suggested_actions", "top_themes", "pain_points", "delighters"]:
                df[col] = df[col].apply(safe_parse)
            return df
    st.error("CSV not found.")
    st.stop()


df = load_data()

all_actions = []
for _, row in df.iterrows():
    for a in row["suggested_actions"]:
        all_actions.append(a)
actions_flat = pd.DataFrame(all_actions) if all_actions else pd.DataFrame(columns=["owner", "action", "priority"])

total = len(df)
pos = (df["sentiment"] == "positive").sum()
neg = (df["sentiment"] == "negative").sum()
p0_count = int((actions_flat["priority"] == "P0").sum()) if len(actions_flat) else 0
p1_count = int((actions_flat["priority"] == "P1").sum()) if len(actions_flat) else 0
total_actions = len(actions_flat)
apps = sorted(df["app"].unique().tolist())

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-title">VoC Intelligence</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Dashboard", "App Explorer", "Action Board", "Full Results"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-section">Overview</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-stat"><div style="font-size:11px;color:#666">Reviews analyzed</div><div class="sidebar-stat-val">200,000</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-stat"><div style="font-size:11px;color:#666">Apps covered</div><div class="sidebar-stat-val">20</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-stat"><div style="font-size:11px;color:#666">Actions flagged</div><div class="sidebar-stat-val">{total_actions}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-stat"><div style="font-size:11px;color:#666">Architecture</div><div style="font-size:13px;color:#aaa;margin-top:2px">FLAN-T5 + LoRA</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-stat"><div style="font-size:11px;color:#666">Training steps</div><div style="font-size:13px;color:#aaa;margin-top:2px">3,449 · Tesla T4 GPU</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-stat"><div style="font-size:11px;color:#666">Test accuracy</div><div style="font-size:13px;color:#aaa;margin-top:2px">85.74%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;color:#444;text-align:center">Tanushree Poojary · UIUC 2026</p>', unsafe_allow_html=True)


# DASHBOARD PAGE
if page == "Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > Dashboard</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Total bundles</div>
            <div class="metric-value">{total}</div>
            <div class="metric-trend-pos">+ 100 samples processed</div>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Positive sentiment</div>
            <div class="metric-value">{pos}</div>
            <div class="metric-trend-pos">50% of all bundles</div>
        </div>''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Negative sentiment</div>
            <div class="metric-value">{neg}</div>
            <div class="metric-trend-neg">50% — needs attention</div>
        </div>''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''<div class="metric-card-dark">
            <div class="metric-label-dark">Critical P0 issues</div>
            <div class="metric-value-dark">{p0_count}</div>
            <div style="font-size:12px;color:#e57373;margin-top:6px">Fix immediately</div>
        </div>''', unsafe_allow_html=True)

    st.write("")

    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown('<div class="chart-card"><div class="chart-title">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app", "sentiment"]).size().unstack(fill_value=0)
        st.bar_chart(app_sent, height=300, color=["#e57373", "#4caf82"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-card"><div class="chart-title">Sentiment split</div>', unsafe_allow_html=True)
        sent_counts = df["sentiment"].value_counts().reset_index()
        sent_counts.columns = ["sentiment", "count"]
        st.bar_chart(sent_counts.set_index("sentiment"), height=130, color=["#e8634a"])
        st.markdown('<div class="divider"></div><div class="chart-title">Action owners</div>', unsafe_allow_html=True)
        if len(actions_flat):
            owner_counts = actions_flat["owner"].value_counts().reset_index()
            owner_counts.columns = ["owner", "count"]
            st.bar_chart(owner_counts.set_index("owner"), height=130, color=["#1a1a2e"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="chart-card"><div class="chart-title">Priority distribution</div>', unsafe_allow_html=True)
        if len(actions_flat):
            prio_counts = actions_flat["priority"].value_counts().reset_index()
            prio_counts.columns = ["priority", "count"]
            st.bar_chart(prio_counts.set_index("priority"), height=200, color=["#e8634a"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card"><div class="chart-title">Top P0 critical actions</div>', unsafe_allow_html=True)
        p0_actions = [a for a in all_actions if a.get("priority") == "P0"]
        for a in p0_actions:
            oc = {"Engineering": "eng", "Product": "prd", "Design": "des"}.get(a.get("owner",""), "eng")
            st.markdown(
                f'<div class="action-row"><span class="badge p0">P0</span><span class="badge {oc}">{a.get("owner","")}</span>{a.get("action","")}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


# APP EXPLORER PAGE
elif page == "App Explorer":
    st.markdown('<div class="page-title">App Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > App Explorer</div>', unsafe_allow_html=True)

    selected_app = st.selectbox("Select an app to analyze", apps)
    app_df = df[df["app"] == selected_app]
    app_actions = [a for _, row in app_df.iterrows() for a in row["suggested_actions"]]
    pos_pct = round((app_df["sentiment"] == "positive").mean() * 100)
    p0_app = sum(1 for a in app_actions if a.get("priority") == "P0")
    p1_app = sum(1 for a in app_actions if a.get("priority") == "P1")

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Bundles analyzed</div><div class="metric-value">{len(app_df)}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Positive sentiment</div><div class="metric-value">{pos_pct}%</div><div class="metric-trend-{"pos" if pos_pct>=50 else "neg"}">{"Good signal" if pos_pct>=50 else "Needs attention"}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">P0 critical</div><div class="metric-value">{p0_app}</div><div class="metric-trend-neg">Fix immediately</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card-dark"><div class="metric-label-dark">P1 this sprint</div><div class="metric-value-dark">{p1_app}</div></div>', unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="chart-card"><div class="chart-title">Top pain points</div>', unsafe_allow_html=True)
        pains = [p for _, row in app_df.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"], list) else []) if isinstance(p, str) and len(p) > 10]
        for p in pains[:5]:
            st.markdown(f'<div class="pain-row">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains:
            st.caption("No pain points detected")
        st.markdown('<div class="divider"></div><div class="chart-title">Top delighters</div>', unsafe_allow_html=True)
        delights = [d for _, row in app_df.iterrows() for d in (row["delighters"] if isinstance(row["delighters"], list) else []) if isinstance(d, str) and len(d) > 10]
        for d in delights[:5]:
            st.markdown(f'<div class="delight-row">{d[:160]}</div>', unsafe_allow_html=True)
        if not delights:
            st.caption("No delighters detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-card"><div class="chart-title">Recommended actions</div>', unsafe_allow_html=True)
        if app_actions:
            for a in app_actions:
                oc = {"Engineering": "eng", "Product": "prd", "Design": "des"}.get(a.get("owner",""), "eng")
                pc = {"P0": "p0", "P1": "p1", "P2": "p2"}.get(a.get("priority",""), "p1")
                st.markdown(f'<div class="action-row"><span class="badge {pc}">{a.get("priority","")}</span><span class="badge {oc}">{a.get("owner","")}</span>{a.get("action","")}</div>', unsafe_allow_html=True)
        else:
            st.caption("No actions flagged")
        st.markdown('<div class="divider"></div><div class="chart-title">AI summaries</div>', unsafe_allow_html=True)
        for _, row in app_df.head(5).iterrows():
            bc = "pos" if row["sentiment"] == "positive" else "neg"
            st.markdown(f'<div class="summary-row"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ACTION BOARD PAGE
elif page == "Action Board":
    st.markdown('<div class="page-title">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > Action Board</div>', unsafe_allow_html=True)

    st.write("")
    col_filter = st.columns(3)
    with col_filter[0]:
        prio_filter = st.multiselect("Priority", ["P0", "P1", "P2"], default=["P0", "P1", "P2"])
    with col_filter[1]:
        owner_filter = st.multiselect("Owner", ["Engineering", "Product", "Design"], default=["Engineering", "Product", "Design"])
    with col_filter[2]:
        app_filter = st.multiselect("App", apps, default=[])

    filtered = actions_flat.copy()
    if prio_filter:
        filtered = filtered[filtered["priority"].isin(prio_filter)]
    if owner_filter:
        filtered = filtered[filtered["owner"].isin(owner_filter)]

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total actions</div><div class="metric-value">{len(filtered)}</div></div>', unsafe_allow_html=True)
    with c2:
        p0_f = (filtered["priority"] == "P0").sum() if len(filtered) else 0
        st.markdown(f'<div class="metric-card"><div class="metric-label">P0 critical</div><div class="metric-value">{p0_f}</div><div class="metric-trend-neg">Fix immediately</div></div>', unsafe_allow_html=True)
    with c3:
        eng_f = (filtered["owner"] == "Engineering").sum() if len(filtered) else 0
        st.markdown(f'<div class="metric-card-dark"><div class="metric-label-dark">Engineering actions</div><div class="metric-value-dark">{eng_f}</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="chart-card"><div class="chart-title">All actions</div>', unsafe_allow_html=True)
    if len(filtered):
        for _, row in filtered.sort_values("priority").iterrows():
            oc = {"Engineering": "eng", "Product": "prd", "Design": "des"}.get(row["owner"], "eng")
            pc = {"P0": "p0", "P1": "p1", "P2": "p2"}.get(row["priority"], "p1")
            st.markdown(
                f'<div class="action-row"><span class="badge {pc}">{row["priority"]}</span><span class="badge {oc}">{row["owner"]}</span>{row["action"]}</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("No actions match your filters")
    st.markdown('</div>', unsafe_allow_html=True)


# FULL RESULTS PAGE
elif page == "Full Results":
    st.markdown('<div class="page-title">Full Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > Full Results</div>', unsafe_allow_html=True)

    st.write("")
    col_f = st.columns(2)
    with col_f[0]:
        sent_f = st.multiselect("Sentiment", ["positive", "negative"], default=["positive", "negative"])
    with col_f[1]:
        app_f = st.multiselect("App", apps, default=[])

    result_df = df.copy()
    if sent_f:
        result_df = result_df[result_df["sentiment"].isin(sent_f)]
    if app_f:
        result_df = result_df[result_df["app"].isin(app_f)]

    st.caption(f"Showing {len(result_df)} of {total} bundles")
    display = result_df[["app", "sentiment", "summary"]].copy()
    display.columns = ["App", "Sentiment", "AI Summary"]
    st.dataframe(display, use_container_width=True, height=500, hide_index=True)

    st.download_button(
        "Download results CSV",
        df.to_csv(index=False),
        "voc_results.csv",
        "text/csv"
    )
