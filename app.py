import streamlit as st
import pandas as pd
import ast
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="VoC Daily Brief", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}

.main{background:#f7f7f5;}
.main .block-container{background:#f7f7f5;padding:2rem 2.5rem;max-width:100%;}

section[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid #e8e8e4!important;min-width:220px!important;max-width:220px!important;}
section[data-testid="stSidebar"]>div{padding:1.8rem 1.2rem;}
section[data-testid="stSidebar"] *{color:#6b7280!important;}

.logo{font-size:16px;font-weight:700;color:#111!important;letter-spacing:-.3px;padding-bottom:20px;border-bottom:1px solid #f0f0ec;margin-bottom:20px;}
.logo span{color:#6366f1!important;}

.nav-item{display:block;padding:8px 10px;border-radius:6px;font-size:13px;font-weight:500;color:#6b7280!important;margin-bottom:2px;cursor:pointer;}
.nav-active{background:#f0f0ec;color:#111!important;font-weight:600;}

.nav-section{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#c4c4bc!important;margin:20px 0 6px 10px;}

.sstat{padding:8px 10px;margin-bottom:4px;}
.sstat-l{font-size:11px;color:#c4c4bc!important;}
.sstat-v{font-size:13px;font-weight:600;color:#374151!important;margin-top:1px;}

/* KPI cards — Notion style */
.kpi{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;border:1px solid #e8e8e4;position:relative;}
.kpi-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#9ca3af;margin-bottom:10px;}
.kpi-value{font-size:36px;font-weight:700;color:#111;line-height:1;letter-spacing:-1px;}
.kpi-sub{font-size:12px;color:#9ca3af;margin-top:8px;}
.kpi-dot{position:absolute;top:1.2rem;right:1.4rem;width:8px;height:8px;border-radius:50%;}
.dot-green{background:#10b981;}
.dot-red{background:#ef4444;}
.dot-amber{background:#f59e0b;}
.dot-gray{background:#d1d5db;}
.kpi-bar{position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:8px 0 0 8px;}
.bar-green{background:#10b981;}
.bar-red{background:#ef4444;}
.bar-amber{background:#f59e0b;}
.bar-blue{background:#6366f1;}

/* Chart cards */
.cc{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;border:1px solid #e8e8e4;margin-top:.8rem;}
.cc-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#9ca3af;margin-bottom:1rem;}
.cc-subtitle{font-size:13px;font-weight:600;color:#111;margin-bottom:.3rem;}
.cc-sub{font-size:12px;color:#9ca3af;margin-bottom:1rem;}

/* Page header */
.ph{font-size:22px;font-weight:700;color:#111;letter-spacing:-.5px;margin:0;}
.pb{font-size:12px;color:#9ca3af;margin-bottom:1.5rem;margin-top:2px;}

/* Divider */
.div{border:none;border-top:1px solid #e8e8e4;margin:1rem 0;}

/* Badges */
.badge{display:inline-block;padding:2px 7px;border-radius:4px;font-size:11px;font-weight:500;margin:2px;}
.pos{background:#ecfdf5;color:#065f46;}
.neg{background:#fef2f2;color:#991b1b;}
.p0{background:#fef2f2;color:#991b1b;font-weight:700;}
.p1{background:#fffbeb;color:#92400e;}
.p2{background:#ecfdf5;color:#065f46;}
.eng{background:#eff6ff;color:#1e40af;}
.prd{background:#f5f3ff;color:#5b21b6;}
.des{background:#fdf2f8;color:#9d174d;}

/* Rows */
.arow{border:1px solid #f0f0ec;border-radius:6px;padding:9px 12px;margin:4px 0;font-size:13px;color:#374151;background:#fafaf9;}
.prow{border-left:2px solid #ef4444;background:#fef9f9;border-radius:0 6px 6px 0;padding:8px 12px;margin:4px 0;font-size:13px;color:#374151;}
.drow{border-left:2px solid #10b981;background:#f9fefb;border-radius:0 6px 6px 0;padding:8px 12px;margin:4px 0;font-size:13px;color:#374151;}
.srow{border:1px solid #f0f0ec;border-radius:6px;padding:9px 12px;margin:4px 0;font-size:13px;color:#374151;background:#fafaf9;}

/* Insight box */
.insight{background:#fafaf9;border:1px solid #e8e8e4;border-left:3px solid #6366f1;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;font-size:13px;color:#374151;line-height:1.6;}
.insight-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6366f1;margin-bottom:4px;}
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
af = pd.DataFrame(all_actions) if all_actions else pd.DataFrame(columns=["owner","action","priority"])
total = len(df)
pos = int((df["sentiment"]=="positive").sum())
neg = int((df["sentiment"]=="negative").sum())
p0c = int((af["priority"]=="P0").sum()) if len(af) else 0
p1c = int((af["priority"]=="P1").sum()) if len(af) else 0
ta = len(af)
apps = sorted(df["app"].unique().tolist())

FONT = dict(family="Inter", size=11, color="#6b7280")
BG = "#fff"
GRID = "#f5f5f3"


def kpi(label, value, sub, bar_class, dot_class):
    return f'''<div class="kpi">
        <div class="kpi-bar {bar_class}"></div>
        <div class="kpi-dot {dot_class}"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>'''


# SIDEBAR
with st.sidebar:
    st.markdown('<div class="logo">VoC <span>Intelligence</span></div>', unsafe_allow_html=True)

    page = st.radio("", ["Daily Brief", "App Deep Dive", "Action Board", "Full Data"],
                    label_visibility="collapsed")

    st.markdown('<div class="nav-section">Dataset</div>', unsafe_allow_html=True)
    for l, v in [("Reviews analyzed", "200,000"), ("Apps", "20"),
                 ("Bundles", str(total)), ("Actions flagged", str(ta))]:
        st.markdown(f'<div class="sstat"><div class="sstat-l">{l}</div><div class="sstat-v">{v}</div></div>',
                    unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Model</div>', unsafe_allow_html=True)
    for l, v in [("FLAN-T5 + LoRA", "85.74% accuracy"),
                 ("Training", "3,449 steps · T4 GPU")]:
        st.markdown(f'<div class="sstat"><div class="sstat-l">{l}</div><div class="sstat-v">{v}</div></div>',
                    unsafe_allow_html=True)

    st.markdown('<br><p style="font-size:11px;color:#d1d5db;text-align:center;padding-top:1rem;border-top:1px solid #f0f0ec">Tanushree Poojary · UIUC 2026</p>',
                unsafe_allow_html=True)


# PAGE 1 — DAILY BRIEF
if page == "Daily Brief":
    st.markdown('<div class="ph">Daily Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="pb">What users are saying across 20 apps — updated each run</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("Reviews processed", "200K", "Google Play · 20 apps", "bar-blue", "dot-gray"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Positive sentiment", f"{pos}", f"{round(pos/total*100)}% of bundles", "bar-green", "dot-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Negative sentiment", f"{neg}", f"{round(neg/total*100)}% needs attention", "bar-red", "dot-red"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Critical P0 issues", f"{p0c}", "Fix before next sprint", "bar-amber", "dot-red"), unsafe_allow_html=True)

    st.write("")

    # Key insight
    st.markdown('''<div class="insight">
        <div class="insight-label">AI Insight</div>
        Sentiment is evenly split — 50% positive, 50% negative. Engineering owns 54% of all recommended actions,
        suggesting product quality issues are driving dissatisfaction more than design or strategy gaps.
        3 P0 issues require immediate attention before the next release.
    </div>''', unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown('<div class="cc"><div class="cc-title">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app", "sentiment"]).size().reset_index(name="count")
        fig = px.bar(app_sent, x="app", y="count", color="sentiment",
                     color_discrete_map={"positive": "#10b981", "negative": "#ef4444"},
                     barmode="group", height=260)
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=70),
            plot_bgcolor=BG, paper_bgcolor=BG,
            font=FONT,
            legend=dict(orientation="h", y=-0.35, x=0, bgcolor="rgba(0,0,0,0)",
                        title_text="", font=dict(size=11)),
            xaxis=dict(showgrid=False, tickangle=-40, title="", linecolor=GRID),
            yaxis=dict(showgrid=True, gridcolor=GRID, title="", linecolor=GRID),
            bargap=0.3, bargroupgap=0.1
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cc"><div class="cc-title">Cumulative sentiment trend</div>', unsafe_allow_html=True)
        trend = df.sort_values("sample_id").copy()
        trend["Positive"] = (trend["sentiment"] == "positive").cumsum()
        trend["Negative"] = (trend["sentiment"] == "negative").cumsum()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=trend["sample_id"], y=trend["Positive"], name="Positive",
            line=dict(color="#10b981", width=2), mode="lines",
            fill="tozeroy", fillcolor="rgba(16,185,129,0.06)"
        ))
        fig2.add_trace(go.Scatter(
            x=trend["sample_id"], y=trend["Negative"], name="Negative",
            line=dict(color="#ef4444", width=2), mode="lines",
            fill="tozeroy", fillcolor="rgba(239,68,68,0.06)"
        ))
        fig2.update_layout(
            height=180, margin=dict(l=0, r=0, t=0, b=30),
            plot_bgcolor=BG, paper_bgcolor=BG, font=FONT,
            legend=dict(orientation="h", y=-0.4, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, title="Bundle ID", linecolor=GRID),
            yaxis=dict(showgrid=True, gridcolor=GRID, linecolor=GRID)
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="cc"><div class="cc-title">Sentiment split</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=["Positive", "Negative"], values=[pos, neg],
            marker=dict(colors=["#10b981", "#ef4444"],
                        line=dict(color="#fff", width=3)),
            hole=0.65,
            textinfo="percent",
            textfont=dict(family="Inter", size=13, color="#fff"),
            hovertemplate="%{label}: %{value}<extra></extra>"
        ))
        fig3.add_annotation(text=f"<b>{round(pos/total*100)}%</b><br>positive",
                            x=0.5, y=0.5, showarrow=False,
                            font=dict(family="Inter", size=14, color="#111"))
        fig3.update_layout(
            height=220, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor=BG, showlegend=True,
            legend=dict(orientation="h", x=0, y=-0.1, font=dict(size=11)),
            font=dict(family="Inter")
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cc"><div class="cc-title">Action owners</div>', unsafe_allow_html=True)
        if len(af):
            oc = af["owner"].value_counts().reset_index()
            oc.columns = ["owner", "count"]
            fig4 = px.bar(oc, x="count", y="owner", orientation="h",
                          color="owner",
                          color_discrete_map={"Engineering": "#6366f1",
                                              "Product": "#8b5cf6",
                                              "Design": "#ec4899"},
                          height=140)
            fig4.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor=BG, paper_bgcolor=BG,
                showlegend=False, font=FONT,
                xaxis=dict(showgrid=True, gridcolor=GRID),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cc"><div class="cc-title">Priority breakdown</div>', unsafe_allow_html=True)
        if len(af):
            pc = af["priority"].value_counts().reset_index()
            pc.columns = ["priority", "count"]
            fig5 = px.bar(pc, x="priority", y="count",
                          color="priority",
                          color_discrete_map={"P0": "#ef4444", "P1": "#f59e0b", "P2": "#10b981"},
                          height=140, text="count")
            fig5.update_traces(textposition="outside",
                               textfont=dict(family="Inter", size=12, color="#374151"))
            fig5.update_layout(
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor=BG, paper_bgcolor=BG,
                showlegend=False, font=FONT,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False, visible=False)
            )
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


# PAGE 2 — APP DEEP DIVE
elif page == "App Deep Dive":
    st.markdown('<div class="ph">App Deep Dive</div>', unsafe_allow_html=True)
    st.markdown('<div class="pb">Drill into any app to see pain points, delighters and recommended actions</div>', unsafe_allow_html=True)

    sel = st.selectbox("", apps, label_visibility="collapsed")
    adf = df[df["app"] == sel]
    aacts = [a for _, row in adf.iterrows() for a in row["suggested_actions"]]
    pp = round((adf["sentiment"] == "positive").mean() * 100)
    p0a = sum(1 for a in aacts if a.get("priority") == "P0")
    p1a = sum(1 for a in aacts if a.get("priority") == "P1")

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("Bundles analyzed", str(len(adf)), f"for {sel}", "bar-blue", "dot-gray"), unsafe_allow_html=True)
    with c2:
        dc = "bar-green" if pp >= 50 else "bar-red"
        dd = "dot-green" if pp >= 50 else "dot-red"
        st.markdown(kpi("Positive sentiment", f"{pp}%", "Good signal" if pp >= 50 else "Needs attention", dc, dd), unsafe_allow_html=True)
    with c3: st.markdown(kpi("P0 critical", str(p0a), "Fix immediately", "bar-red", "dot-red"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("P1 this sprint", str(p1a), "Address soon", "bar-amber", "dot-amber"), unsafe_allow_html=True)

    st.write("")
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="cc"><div class="cc-title">Pain points</div>', unsafe_allow_html=True)
        pains = [p for _, row in adf.iterrows()
                 for p in (row["pain_points"] if isinstance(row["pain_points"], list) else [])
                 if isinstance(p, str) and len(p) > 10]
        for p in pains[:6]:
            st.markdown(f'<div class="prow">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains: st.caption("No pain points detected")

        st.markdown('<div style="margin-top:1rem" class="cc-title">Delighters</div>', unsafe_allow_html=True)
        dels = [d for _, row in adf.iterrows()
                for d in (row["delighters"] if isinstance(row["delighters"], list) else [])
                if isinstance(d, str) and len(d) > 10]
        for d in dels[:6]:
            st.markdown(f'<div class="drow">{d[:160]}</div>', unsafe_allow_html=True)
        if not dels: st.caption("No delighters detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="cc"><div class="cc-title">Recommended actions</div>', unsafe_allow_html=True)
        if aacts:
            for a in aacts:
                oc2 = {"Engineering": "eng", "Product": "prd", "Design": "des"}.get(a.get("owner", ""), "eng")
                pc2 = {"P0": "p0", "P1": "p1", "P2": "p2"}.get(a.get("priority", ""), "p1")
                st.markdown(f'<div class="arow"><span class="badge {pc2}">{a.get("priority","")}</span> <span class="badge {oc2}">{a.get("owner","")}</span> {a.get("action","")}</div>',
                            unsafe_allow_html=True)
        else:
            st.caption("No actions flagged for this app")

        st.markdown('<div style="margin-top:1rem" class="cc-title">AI summaries</div>', unsafe_allow_html=True)
        for _, row in adf.head(6).iterrows():
            bc = "pos" if row["sentiment"] == "positive" else "neg"
            st.markdown(f'<div class="srow"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# PAGE 3 — ACTION BOARD
elif page == "Action Board":
    st.markdown('<div class="ph">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="pb">All recommended actions filtered by priority and owner — use this for sprint planning</div>', unsafe_allow_html=True)

    st.write("")
    f1, f2 = st.columns(2)
    with f1: pf = st.multiselect("Priority", ["P0", "P1", "P2"], default=["P0", "P1", "P2"])
    with f2: of = st.multiselect("Owner", ["Engineering", "Product", "Design"],
                                  default=["Engineering", "Product", "Design"])

    filt = af.copy()
    if pf: filt = filt[filt["priority"].isin(pf)]
    if of: filt = filt[filt["owner"].isin(of)]

    st.write("")
    c1, c2, c3 = st.columns(3)
    p0f = int((filt["priority"] == "P0").sum()) if len(filt) else 0
    engf = int((filt["owner"] == "Engineering").sum()) if len(filt) else 0
    with c1: st.markdown(kpi("Total actions", str(len(filt)), "in current filter", "bar-blue", "dot-gray"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("P0 critical", str(p0f), "Fix before shipping", "bar-red", "dot-red"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Engineering items", str(engf), "of filtered actions", "bar-blue", "dot-gray"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="cc"><div class="cc-title">Actions</div>', unsafe_allow_html=True)
    if len(filt):
        for _, row in filt.sort_values("priority").iterrows():
            oc2 = {"Engineering": "eng", "Product": "prd", "Design": "des"}.get(row["owner"], "eng")
            pc2 = {"P0": "p0", "P1": "p1", "P2": "p2"}.get(row["priority"], "p1")
            st.markdown(f'<div class="arow"><span class="badge {pc2}">{row["priority"]}</span> <span class="badge {oc2}">{row["owner"]}</span> {row["action"]}</div>',
                        unsafe_allow_html=True)
    else:
        st.caption("No actions match your filters")
    st.markdown('</div>', unsafe_allow_html=True)


# PAGE 4 — FULL DATA
elif page == "Full Data":
    st.markdown('<div class="ph">Full Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="pb">Complete results table — filter and export</div>', unsafe_allow_html=True)

    st.write("")
    f1, f2 = st.columns(2)
    with f1: sf = st.multiselect("Sentiment", ["positive", "negative"], default=["positive", "negative"])
    with f2: appf = st.multiselect("App", apps, default=[])

    rdf = df.copy()
    if sf: rdf = rdf[rdf["sentiment"].isin(sf)]
    if appf: rdf = rdf[rdf["app"].isin(appf)]

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi("Showing", str(len(rdf)), "of 100 bundles", "bar-blue", "dot-gray"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Positive", str((rdf["sentiment"] == "positive").sum()), "in selection", "bar-green", "dot-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Negative", str((rdf["sentiment"] == "negative").sum()), "in selection", "bar-red", "dot-red"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="cc"><div class="cc-title">Results</div>', unsafe_allow_html=True)
    disp = rdf[["app", "sentiment", "summary"]].copy()
    disp.columns = ["App", "Sentiment", "AI Summary"]
    st.dataframe(disp, use_container_width=True, height=460, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.download_button("Download CSV", df.to_csv(index=False), "voc_results.csv", "text/csv")
