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
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1c1c2e !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }
section[data-testid="stSidebar"] * { color: #c8c8e0 !important; }

/* Main background */
.main .block-container { background: #f4f6f9; padding: 2rem 2.5rem; max-width: 100%; }

/* Metric cards */
.mcard {
    background: #fff;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    border: 1px solid #ebebeb;
    position: relative;
    overflow: hidden;
    height: 130px;
}
.mcard-dark {
    background: #1c1c2e;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    border: none;
    position: relative;
    overflow: hidden;
    height: 130px;
}
.mcard-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #999;
    margin-bottom: 8px;
}
.mcard-label-dark {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #555;
    margin-bottom: 8px;
}
.mcard-val { font-size: 36px; font-weight: 700; color: #1c1c2e; line-height: 1; }
.mcard-val-dark { font-size: 36px; font-weight: 700; color: #fff; line-height: 1; }
.mcard-sub-green { font-size: 12px; color: #4caf82; font-weight: 500; margin-top: 8px; }
.mcard-sub-red { font-size: 12px; color: #e57373; font-weight: 500; margin-top: 8px; }
.mcard-sub-gray { font-size: 12px; color: #999; font-weight: 500; margin-top: 8px; }
.mcard-icon-green {
    position: absolute; top: 1.4rem; right: 1.4rem;
    width: 44px; height: 44px; border-radius: 50%;
    background: #e8f5ee;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.mcard-icon-red {
    position: absolute; top: 1.4rem; right: 1.4rem;
    width: 44px; height: 44px; border-radius: 50%;
    background: #fdecea;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.mcard-icon-orange {
    position: absolute; top: 1.4rem; right: 1.4rem;
    width: 44px; height: 44px; border-radius: 50%;
    background: #fff3e0;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.mcard-icon-dark {
    position: absolute; top: 1.4rem; right: 1.4rem;
    width: 44px; height: 44px; border-radius: 50%;
    background: #2e2e4e;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}

/* Chart cards */
.ccard {
    background: #fff;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    border: 1px solid #ebebeb;
    margin-top: 1rem;
}
.ccard-dark {
    background: #1c1c2e;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
}
.ccard-title {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #999;
    margin-bottom: 1rem;
}
.ccard-title-dark {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #555;
    margin-bottom: 1rem;
}

/* Page title */
.page-title { font-size: 22px; font-weight: 700; color: #1c1c2e; margin: 0; }
.breadcrumb { font-size: 12px; color: #aaa; margin-bottom: 1.5rem; }

/* Badges */
.badge { display:inline-block; padding:3px 9px; border-radius:5px; font-size:11px; font-weight:600; margin:2px; }
.pos { background:#e8f5ee; color:#2e7d52; }
.neg { background:#fdecea; color:#c62828; }
.p0  { background:#fdecea; color:#c62828; }
.p1  { background:#fff3e0; color:#e65100; }
.p2  { background:#e8f5ee; color:#2e7d52; }
.eng { background:#e3f2fd; color:#1565c0; }
.prd { background:#f3e5f5; color:#6a1b9a; }
.des { background:#fce4ec; color:#880e4f; }

/* Rows */
.action-row { background:#fafafa; border:1px solid #f0f0f0; border-radius:8px; padding:10px 14px; margin:5px 0; font-size:13px; color:#333; }
.pain-row { border-left:3px solid #e57373; background:#fff8f8; border-radius:0 8px 8px 0; padding:8px 12px; margin:5px 0; font-size:13px; color:#444; }
.delight-row { border-left:3px solid #4caf82; background:#f8fff9; border-radius:0 8px 8px 0; padding:8px 12px; margin:5px 0; font-size:13px; color:#444; }
.summary-row { background:#fafafa; border:1px solid #f0f0f0; border-radius:8px; padding:10px 14px; margin:5px 0; font-size:13px; color:#444; }

/* Sidebar nav */
.snav { display:block; padding:10px 14px; border-radius:8px; font-size:14px; font-weight:500; margin-bottom:4px; color:#c8c8e0; cursor:pointer; }
.snav-active { background:#e8634a; color:#fff !important; }
.ssection { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.1em; color:#444 !important; margin:1.2rem 0 .5rem; }
.sstat { background:#12122a; border-radius:8px; padding:10px 14px; margin-bottom:8px; }
.sstat-label { font-size:11px; color:#555 !important; }
.sstat-val { font-size:20px; font-weight:700; color:#fff !important; }
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
            def sp(v):
                try: return ast.literal_eval(v)
                except: return []
            for c in ["suggested_actions","top_themes","pain_points","delighters"]:
                df[c] = df[c].apply(sp)
            return df
    st.error("CSV not found.")
    st.stop()


df = load_data()

all_actions = [a for _, row in df.iterrows() for a in row["suggested_actions"]]
actions_flat = pd.DataFrame(all_actions) if all_actions else pd.DataFrame(columns=["owner","action","priority"])

total = len(df)
pos = int((df["sentiment"]=="positive").sum())
neg = int((df["sentiment"]=="negative").sum())
p0_count = int((actions_flat["priority"]=="P0").sum()) if len(actions_flat) else 0
p1_count = int((actions_flat["priority"]=="P1").sum()) if len(actions_flat) else 0
total_actions = len(actions_flat)
apps = sorted(df["app"].unique().tolist())

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='font-size:20px;font-weight:700;color:#fff;padding-bottom:12px;border-bottom:1px solid #2e2e4e;margin-bottom:16px'>
        VoC Intelligence
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["Dashboard", "App Explorer", "Action Board", "Full Results"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="ssection">Overview</div>', unsafe_allow_html=True)
    for label, val in [("Reviews analyzed","200,000"),("Apps covered","20"),("Actions flagged",str(total_actions)),("Bundles processed",str(total))]:
        st.markdown(f'<div class="sstat"><div class="sstat-label">{label}</div><div class="sstat-val">{val}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="ssection">Model</div>', unsafe_allow_html=True)
    for label, val in [("Architecture","FLAN-T5 + LoRA"),("Checkpoint","3,449 steps"),("GPU","Tesla T4"),("Accuracy","85.74%")]:
        st.markdown(f'<div class="sstat"><div class="sstat-label">{label}</div><div style="font-size:13px;color:#aaa;margin-top:2px">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;color:#333;text-align:center">Tanushree Poojary · UIUC 2026</p>', unsafe_allow_html=True)


# DASHBOARD
if page == "Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > Dashboard</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''<div class="mcard">
            <div class="mcard-label">Total bundles</div>
            <div class="mcard-val">{total}</div>
            <div class="mcard-sub-green">+ 100 samples processed</div>
            <div class="mcard-icon-green">&#x1F4CA;</div>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="mcard">
            <div class="mcard-label">Positive sentiment</div>
            <div class="mcard-val">{pos}</div>
            <div class="mcard-sub-green">+{round(pos/total*100)}% of all bundles</div>
            <div class="mcard-icon-green">&#x2B06;</div>
        </div>''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''<div class="mcard">
            <div class="mcard-label">Negative sentiment</div>
            <div class="mcard-val">{neg}</div>
            <div class="mcard-sub-red">-{round(neg/total*100)}% needs attention</div>
            <div class="mcard-icon-red">&#x2B07;</div>
        </div>''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''<div class="mcard-dark">
            <div class="mcard-label-dark">Critical P0 issues</div>
            <div class="mcard-val-dark">{p0_count}</div>
            <div class="mcard-sub-red">Fix immediately</div>
            <div class="mcard-icon-dark">&#x26A0;</div>
        </div>''', unsafe_allow_html=True)

    st.write("")

    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app","sentiment"]).size().unstack(fill_value=0)
        st.bar_chart(app_sent, height=280, color=["#e57373","#4caf82"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment trend across bundles</div>', unsafe_allow_html=True)
        trend = df.sort_values("sample_id").copy()
        trend["positive_running"] = (trend["sentiment"]=="positive").cumsum()
        trend["negative_running"] = (trend["sentiment"]=="negative").cumsum()
        st.line_chart(trend.set_index("sample_id")[["positive_running","negative_running"]], height=200, color=["#4caf82","#e57373"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment split</div>', unsafe_allow_html=True)
        sent_counts = df["sentiment"].value_counts().reset_index()
        sent_counts.columns = ["sentiment","count"]
        st.bar_chart(sent_counts.set_index("sentiment"), height=160, color=["#e8634a"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard"><div class="ccard-title">Action owners</div>', unsafe_allow_html=True)
        if len(actions_flat):
            oc = actions_flat["owner"].value_counts().reset_index()
            oc.columns = ["owner","count"]
            st.bar_chart(oc.set_index("owner"), height=160, color=["#1c1c2e"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard"><div class="ccard-title">Priority breakdown</div>', unsafe_allow_html=True)
        if len(actions_flat):
            pc = actions_flat["priority"].value_counts().reset_index()
            pc.columns = ["priority","count"]
            st.bar_chart(pc.set_index("priority"), height=160, color=["#e8634a"])
        st.markdown('</div>', unsafe_allow_html=True)


# APP EXPLORER
elif page == "App Explorer":
    st.markdown('<div class="page-title">App Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > App Explorer</div>', unsafe_allow_html=True)

    selected_app = st.selectbox("Select an app", apps)
    app_df = df[df["app"]==selected_app]
    app_actions = [a for _, row in app_df.iterrows() for a in row["suggested_actions"]]
    pos_pct = round((app_df["sentiment"]=="positive").mean()*100)
    p0_app = sum(1 for a in app_actions if a.get("priority")=="P0")
    p1_app = sum(1 for a in app_actions if a.get("priority")=="P1")

    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="mcard"><div class="mcard-label">Bundles</div><div class="mcard-val">{len(app_df)}</div><div class="mcard-icon-green">&#x1F4CB;</div></div>', unsafe_allow_html=True)
    with c2:
        col = "mcard-sub-green" if pos_pct >= 50 else "mcard-sub-red"
        st.markdown(f'<div class="mcard"><div class="mcard-label">Positive sentiment</div><div class="mcard-val">{pos_pct}%</div><div class="{col}">{"Good signal" if pos_pct>=50 else "Needs attention"}</div><div class="mcard-icon-{"green" if pos_pct>=50 else "red"}">{"&#x2B06;" if pos_pct>=50 else "&#x2B07;"}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="mcard"><div class="mcard-label">P0 critical</div><div class="mcard-val">{p0_app}</div><div class="mcard-sub-red">Fix immediately</div><div class="mcard-icon-red">&#x26A0;</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="mcard-dark"><div class="mcard-label-dark">P1 this sprint</div><div class="mcard-val-dark">{p1_app}</div><div class="mcard-icon-dark">&#x1F3AF;</div></div>', unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="ccard"><div class="ccard-title">Top pain points</div>', unsafe_allow_html=True)
        pains = [p for _, row in app_df.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"],list) else []) if isinstance(p,str) and len(p)>10]
        for p in pains[:5]:
            st.markdown(f'<div class="pain-row">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains: st.caption("No pain points detected")
        st.markdown('<br><div class="ccard-title">Top delighters</div>', unsafe_allow_html=True)
        dels = [d for _, row in app_df.iterrows() for d in (row["delighters"] if isinstance(row["delighters"],list) else []) if isinstance(d,str) and len(d)>10]
        for d in dels[:5]:
            st.markdown(f'<div class="delight-row">{d[:160]}</div>', unsafe_allow_html=True)
        if not dels: st.caption("No delighters detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ccard"><div class="ccard-title">Recommended actions</div>', unsafe_allow_html=True)
        if app_actions:
            for a in app_actions:
                oc = {"Engineering":"eng","Product":"prd","Design":"des"}.get(a.get("owner",""),"eng")
                pc = {"P0":"p0","P1":"p1","P2":"p2"}.get(a.get("priority",""),"p1")
                st.markdown(f'<div class="action-row"><span class="badge {pc}">{a.get("priority","")}</span> <span class="badge {oc}">{a.get("owner","")}</span> {a.get("action","")}</div>', unsafe_allow_html=True)
        else:
            st.caption("No actions flagged")
        st.markdown('<br><div class="ccard-title">AI summaries</div>', unsafe_allow_html=True)
        for _, row in app_df.head(5).iterrows():
            bc = "pos" if row["sentiment"]=="positive" else "neg"
            st.markdown(f'<div class="summary-row"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ACTION BOARD
elif page == "Action Board":
    st.markdown('<div class="page-title">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > Action Board</div>', unsafe_allow_html=True)

    st.write("")
    f1, f2 = st.columns(2)
    with f1:
        pf = st.multiselect("Priority", ["P0","P1","P2"], default=["P0","P1","P2"])
    with f2:
        of = st.multiselect("Owner", ["Engineering","Product","Design"], default=["Engineering","Product","Design"])

    filtered = actions_flat.copy()
    if pf: filtered = filtered[filtered["priority"].isin(pf)]
    if of: filtered = filtered[filtered["owner"].isin(of)]

    st.write("")
    c1,c2,c3 = st.columns(3)
    p0_f = int((filtered["priority"]=="P0").sum()) if len(filtered) else 0
    eng_f = int((filtered["owner"]=="Engineering").sum()) if len(filtered) else 0
    with c1:
        st.markdown(f'<div class="mcard"><div class="mcard-label">Total actions</div><div class="mcard-val">{len(filtered)}</div><div class="mcard-icon-orange">&#x1F4CB;</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="mcard"><div class="mcard-label">P0 critical</div><div class="mcard-val">{p0_f}</div><div class="mcard-sub-red">Fix immediately</div><div class="mcard-icon-red">&#x26A0;</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="mcard-dark"><div class="mcard-label-dark">Engineering actions</div><div class="mcard-val-dark">{eng_f}</div><div class="mcard-icon-dark">&#x2699;</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="ccard"><div class="ccard-title">All recommended actions</div>', unsafe_allow_html=True)
    if len(filtered):
        for _, row in filtered.sort_values("priority").iterrows():
            oc = {"Engineering":"eng","Product":"prd","Design":"des"}.get(row["owner"],"eng")
            pc = {"P0":"p0","P1":"p1","P2":"p2"}.get(row["priority"],"p1")
            st.markdown(f'<div class="action-row"><span class="badge {pc}">{row["priority"]}</span> <span class="badge {oc}">{row["owner"]}</span> {row["action"]}</div>', unsafe_allow_html=True)
    else:
        st.caption("No actions match filters")
    st.markdown('</div>', unsafe_allow_html=True)


# FULL RESULTS
elif page == "Full Results":
    st.markdown('<div class="page-title">Full Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home > Full Results</div>', unsafe_allow_html=True)

    st.write("")
    f1, f2 = st.columns(2)
    with f1:
        sf = st.multiselect("Sentiment", ["positive","negative"], default=["positive","negative"])
    with f2:
        af = st.multiselect("App", apps, default=[])

    rdf = df.copy()
    if sf: rdf = rdf[rdf["sentiment"].isin(sf)]
    if af: rdf = rdf[rdf["app"].isin(af)]

    st.caption(f"Showing {len(rdf)} of {total} bundles")
    st.markdown('<div class="ccard">', unsafe_allow_html=True)
    disp = rdf[["app","sentiment","summary"]].copy()
    disp.columns = ["App","Sentiment","AI Summary"]
    st.dataframe(disp, use_container_width=True, height=480, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.download_button("Download results CSV", df.to_csv(index=False), "voc_results.csv", "text/csv")
