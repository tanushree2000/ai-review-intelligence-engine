import streamlit as st
import pandas as pd
import ast
import os

st.set_page_config(
    page_title="VoC Review Intelligence Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.metric-card{background:#1e1e2e;border-radius:10px;padding:1.2rem 1rem;text-align:center;border:1px solid #2e2e3e}
.metric-label{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.metric-value{font-size:30px;font-weight:600;color:#fff}
.badge{display:inline-block;padding:3px 10px;border-radius:5px;font-size:12px;font-weight:500;margin:2px}
.pos{background:#1a3a2a;color:#4caf82}.neg{background:#3a1a1a;color:#e57373}
.mix{background:#3a301a;color:#ffb74d}.p0{background:#3a1a1a;color:#e57373}
.p1{background:#3a301a;color:#ffb74d}.p2{background:#1a3a2a;color:#4caf82}
.eng{background:#1a2a3a;color:#64b5f6}.prd{background:#2a1a3a;color:#ba68c8}.des{background:#3a1a2a;color:#f06292}
.section-header{font-size:13px;font-weight:500;color:#aaa;text-transform:uppercase;letter-spacing:.06em;margin:1.5rem 0 .75rem;padding-bottom:6px;border-bottom:1px solid #2e2e3e}
.pain-item{background:#1e1e2e;border-left:3px solid #e57373;border-radius:0 6px 6px 0;padding:8px 12px;margin:6px 0;font-size:13px;color:#ccc}
.delight-item{background:#1e1e2e;border-left:3px solid #4caf82;border-radius:0 6px 6px 0;padding:8px 12px;margin:6px 0;font-size:13px;color:#ccc}
.summary-item{background:#1e1e2e;border-radius:8px;padding:10px 14px;margin:6px 0;font-size:13px;color:#ccc;border:1px solid #2e2e3e}
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
            for col in ["suggested_actions","top_themes","pain_points","delighters"]:
                df[col] = df[col].apply(safe_parse)
            return df
    st.error("CSV not found. Please upload review_intel_outputs.csv to the repo root or outputs/ folder.")
    st.stop()

df = load_data()

all_actions = []
for _, row in df.iterrows():
    for a in row["suggested_actions"]:
        all_actions.append(a)
actions_flat = pd.DataFrame(all_actions) if all_actions else pd.DataFrame(columns=["owner","action","priority"])

total = len(df)
pos = (df["sentiment"]=="positive").sum()
neg = (df["sentiment"]=="negative").sum()
p0_count = int((actions_flat["priority"]=="P0").sum()) if len(actions_flat) else 0
total_actions = len(actions_flat)

st.markdown("## Voice of Customer — Review Intelligence Engine")
st.markdown("<p style='color:#888;font-size:13px;margin-top:-10px'>AI-powered product analytics · Fine-tuned FLAN-T5 · 200,000 Google Play reviews · 20 apps</p>", unsafe_allow_html=True)
st.divider()

c1,c2,c3,c4,c5 = st.columns(5)
for col, label, val in zip(
    [c1,c2,c3,c4,c5],
    ["Reviews analyzed","Bundles processed","Positive sentiment","Actions generated","Critical P0 issues"],
    ["200K", total, f"{pos}%", total_actions, p0_count]
):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3 = st.tabs(["Dashboard", "Explore by App", "Full Results"])

with tab1:
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-header">Sentiment breakdown</div>', unsafe_allow_html=True)
        sent_counts = df["sentiment"].value_counts().reset_index()
        sent_counts.columns = ["sentiment","count"]
        st.bar_chart(sent_counts.set_index("sentiment"), height=220)

        st.markdown('<div class="section-header">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app","sentiment"]).size().unstack(fill_value=0)
        st.bar_chart(app_sent, height=300)

    with col_r:
        st.markdown('<div class="section-header">Action owners</div>', unsafe_allow_html=True)
        if len(actions_flat):
            owner_counts = actions_flat["owner"].value_counts().reset_index()
            owner_counts.columns = ["owner","count"]
            st.bar_chart(owner_counts.set_index("owner"), height=220)

        st.markdown('<div class="section-header">Priority distribution</div>', unsafe_allow_html=True)
        if len(actions_flat):
            prio_counts = actions_flat["priority"].value_counts().reset_index()
            prio_counts.columns = ["priority","count"]
            st.bar_chart(prio_counts.set_index("priority"), height=300)

    st.divider()
    st.markdown('<div class="section-header">All recommended actions</div>', unsafe_allow_html=True)
    if len(actions_flat):
        st.dataframe(actions_flat[["priority","owner","action"]].sort_values("priority"), use_container_width=True, hide_index=True)

with tab2:
    apps = sorted(df["app"].unique().tolist())
    selected_app = st.selectbox("Select an app", apps)
    app_df = df[df["app"]==selected_app]
    st.markdown(f"<p style='color:#888;font-size:13px'>{len(app_df)} review bundles analyzed for {selected_app}</p>", unsafe_allow_html=True)

    pos_pct = round((app_df["sentiment"]=="positive").mean()*100)
    app_actions = [a for _, row in app_df.iterrows() for a in row["suggested_actions"]]
    p0_app = sum(1 for a in app_actions if a.get("priority")=="P0")

    a1,a2,a3 = st.columns(3)
    for col, label, val in zip([a1,a2,a3], ["Positive sentiment","Negative sentiment","P0 critical issues"], [f"{pos_pct}%", f"{100-pos_pct}%", p0_app]):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)

    st.write("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">Top pain points</div>', unsafe_allow_html=True)
        pains = [p for _, row in app_df.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"], list) else []) if isinstance(p, str) and len(p)>10]
        for p in pains[:5]:
            st.markdown(f'<div class="pain-item">{p[:150]}</div>', unsafe_allow_html=True)
        if not pains:
            st.caption("No pain points detected")

        st.markdown('<div class="section-header">Top delighters</div>', unsafe_allow_html=True)
        delights = [d for _, row in app_df.iterrows() for d in (row["delighters"] if isinstance(row["delighters"], list) else []) if isinstance(d, str) and len(d)>10]
        for d in delights[:5]:
            st.markdown(f'<div class="delight-item">{d[:150]}</div>', unsafe_allow_html=True)
        if not delights:
            st.caption("No delighters detected")

    with col_b:
        st.markdown('<div class="section-header">Recommended actions</div>', unsafe_allow_html=True)
        if app_actions:
            for a in app_actions:
                owner = a.get("owner","")
                action = a.get("action","")
                prio = a.get("priority","")
                oc = {"Engineering":"eng","Product":"prd","Design":"des"}.get(owner,"eng")
                pc = {"P0":"p0","P1":"p1","P2":"p2"}.get(prio,"p1")
                st.markdown(f'<div class="summary-item"><span class="badge {pc}">{prio}</span> <span class="badge {oc}">{owner}</span> &nbsp;{action}</div>', unsafe_allow_html=True)
        else:
            st.caption("No actions flagged for this app")

        st.markdown('<div class="section-header">AI summaries</div>', unsafe_allow_html=True)
        for _, row in app_df.head(5).iterrows():
            sent = row["sentiment"]
            bc = "pos" if sent=="positive" else "neg"
            st.markdown(f'<div class="summary-item"><span class="badge {bc}">{sent}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Full results table</div>', unsafe_allow_html=True)
    display_df = df[["app","sentiment","summary","sample_id"]].copy()
    display_df.columns = ["App","Sentiment","AI Summary","ID"]
    st.dataframe(display_df, use_container_width=True, height=500, hide_index=True)
    st.download_button("Download full results CSV", df.to_csv(index=False), "voc_results.csv", "text/csv")

st.divider()
st.markdown("<p style='color:#555;font-size:12px;text-align:center'>Built by Tanushree Poojary · MS Information Management, UIUC 2026 · Fine-tuned FLAN-T5 with LoRA</p>", unsafe_allow_html=True)
