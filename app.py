
import streamlit as st
import pandas as pd
import ast
import re

st.set_page_config(
    page_title="VoC Review Intelligence Engine",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.metric-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
    border: 0.5px solid #e0e0e0;
}
.metric-label { font-size: 12px; color: #888; margin-bottom: 4px; }
.metric-value { font-size: 28px; font-weight: 600; color: #1a1a1a; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
}
.pos { background: #e1f5ee; color: #085041; }
.neg { background: #fcebeb; color: #791f1f; }
.mix { background: #faeeda; color: #633806; }
.p0  { background: #fcebeb; color: #791f1f; }
.p1  { background: #faeeda; color: #633806; }
.p2  { background: #e1f5ee; color: #085041; }
.eng { background: #e6f1fb; color: #0c447c; }
.prd { background: #eeedfe; color: #3c3489; }
.des { background: #fbeaf0; color: #72243e; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("review_intel_outputs.csv")
    def safe_parse(val):
        try:
            return ast.literal_eval(val)
        except:
            return []
    df["suggested_actions"] = df["suggested_actions"].apply(safe_parse)
    df["top_themes"] = df["top_themes"].apply(safe_parse)
    df["pain_points"] = df["pain_points"].apply(safe_parse)
    df["delighters"] = df["delighters"].apply(safe_parse)
    return df

df = load_data()

st.title("🧠 Voice of Customer — Review Intelligence Engine")
st.caption("AI-powered product analytics · Fine-tuned FLAN-T5 · 200,000 Google Play reviews · 20 apps")

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)
total = len(df)
pos = (df["sentiment"] == "positive").sum()
neg = (df["sentiment"] == "negative").sum()
actions_df = df.explode_actions = []

all_actions = []
for _, row in df.iterrows():
    for a in row["suggested_actions"]:
        all_actions.append(a)
actions_flat = pd.DataFrame(all_actions) if all_actions else pd.DataFrame(columns=["owner","priority","action"])

p0 = (actions_flat["priority"] == "P0").sum() if len(actions_flat) else 0
total_actions = len(actions_flat)

with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">reviews analyzed</div><div class="metric-value">200K</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">bundles processed</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">positive sentiment</div><div class="metric-value">{pos}%</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">actions generated</div><div class="metric-value">{total_actions}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><div class="metric-label">critical P0 issues</div><div class="metric-value">{p0}</div></div>', unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Explore by App", "📋 Full Results"])

with tab1:
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Sentiment breakdown")
        sent_counts = df["sentiment"].value_counts().reset_index()
        sent_counts.columns = ["sentiment", "count"]
        st.bar_chart(sent_counts.set_index("sentiment"))

        st.subheader("Sentiment by app")
        app_sent = df.groupby(["app","sentiment"]).size().unstack(fill_value=0)
        st.bar_chart(app_sent)

    with col_r:
        st.subheader("Action owners")
        if len(actions_flat):
            owner_counts = actions_flat["owner"].value_counts().reset_index()
            owner_counts.columns = ["owner", "count"]
            st.bar_chart(owner_counts.set_index("owner"))

        st.subheader("Priority distribution")
        if len(actions_flat):
            prio_counts = actions_flat["priority"].value_counts().reset_index()
            prio_counts.columns = ["priority", "count"]
            st.bar_chart(prio_counts.set_index("priority"))

with tab2:
    apps = sorted(df["app"].unique().tolist())
    selected_app = st.selectbox("Select an app", apps)

    app_df = df[df["app"] == selected_app]
    st.caption(f"{len(app_df)} review bundles analyzed for {selected_app}")

    a1, a2 = st.columns(2)
    with a1:
        pos_pct = round((app_df["sentiment"] == "positive").mean() * 100)
        neg_pct = 100 - pos_pct
        st.metric("Positive sentiment", f"{pos_pct}%")
        st.metric("Negative sentiment", f"{neg_pct}%")
    with a2:
        app_actions = []
        for _, row in app_df.iterrows():
            for a in row["suggested_actions"]:
                app_actions.append(a)
        if app_actions:
            st.metric("Actions flagged", len(app_actions))
            p0_app = sum(1 for a in app_actions if a.get("priority") == "P0")
            st.metric("P0 critical issues", p0_app)

    st.subheader("Top pain points")
    all_pains = []
    for _, row in app_df.iterrows():
        pains = row["pain_points"]
        if isinstance(pains, list):
            all_pains.extend([p for p in pains if isinstance(p, str) and len(p) > 10])
    if all_pains:
        for p in all_pains[:5]:
            st.markdown(f"- {p[:120]}")
    else:
        st.caption("No pain points detected")

    st.subheader("Top delighters")
    all_delights = []
    for _, row in app_df.iterrows():
        dels = row["delighters"]
        if isinstance(dels, list):
            all_delights.extend([d for d in dels if isinstance(d, str) and len(d) > 10])
    if all_delights:
        for d in all_delights[:5]:
            st.markdown(f"- {d[:120]}")
    else:
        st.caption("No delighters detected")

    st.subheader("Recommended actions")
    if app_actions:
        for a in app_actions:
            owner = a.get("owner","")
            action = a.get("action","")
            prio = a.get("priority","")
            owner_class = {"Engineering":"eng","Product":"prd","Design":"des"}.get(owner,"eng")
            prio_class = {"P0":"p0","P1":"p1","P2":"p2"}.get(prio,"p1")
            st.markdown(
                f'<span class="badge {prio_class}">{prio}</span> &nbsp; '
                f'<span class="badge {owner_class}">{owner}</span> &nbsp; {action}',
                unsafe_allow_html=True
            )
            st.write("")
    else:
        st.caption("No actions flagged for this app")

    st.subheader("Sample summaries")
    for _, row in app_df.head(5).iterrows():
        sent = row["sentiment"]
        badge_class = "pos" if sent == "positive" else "neg" if sent == "negative" else "mix"
        st.markdown(
            f'<span class="badge {badge_class}">{sent}</span> &nbsp; {row["summary"]}',
            unsafe_allow_html=True
        )
        st.write("")

with tab3:
    st.subheader("Full results table")
    display_df = df[["app","sentiment","summary","sample_id"]].copy()
    display_df.columns = ["App","Sentiment","AI Summary","ID"]
    st.dataframe(display_df, use_container_width=True, height=500)

    csv = df.to_csv(index=False)
    st.download_button(
        label="Download full results CSV",
        data=csv,
        file_name="voc_review_intelligence_results.csv",
        mime="text/csv"
    )

st.divider()
st.caption("Built by Tanushree Poojary · MS Information Management, UIUC 2026 · Fine-tuned FLAN-T5 with LoRA · GitHub")
