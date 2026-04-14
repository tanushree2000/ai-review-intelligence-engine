import streamlit as st
import pandas as pd
import ast
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="VoC Intelligence", layout="wide", initial_sidebar_state="expanded", page_icon="🧠")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}

.main{background:#0d0d0d;}
.main .block-container{background:#0d0d0d;padding:0.5rem 1.5rem 2rem;max-width:100%;}
.stApp{background:#0d0d0d!important;}
[data-testid="stAppViewContainer"]{background:#0d0d0d!important;}
[data-testid="stHeader"]{background:#0d0d0d!important;display:none;}
[data-testid="stToolbar"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
.block-container{padding-top:0.5rem!important;}

section[data-testid="stSidebar"]{background:#111111!important;border-right:1px solid #1e1e1e!important;min-width:200px!important;max-width:200px!important;}
section[data-testid="stSidebar"]>div{padding:1rem 0.9rem;}
section[data-testid="stSidebar"] *{color:#6b7280!important;}
section[data-testid="stSidebar"] label{font-size:12px!important;font-weight:500!important;}
section[data-testid="stSidebar"] .stRadio>div{gap:2px!important;}
section[data-testid="stSidebar"] .stRadio label{padding:5px 8px!important;border-radius:6px!important;}
[data-testid="stSidebarNavItems"]{display:none!important;}
div[data-testid="stSidebarNav"]{display:none!important;}
div[data-testid="stSidebarNavSeparator"]{display:none!important;}
[data-testid="stSidebarNavLink"]{display:none!important;}

.brand{font-size:14px;font-weight:700;color:#fff!important;letter-spacing:.2px;padding-bottom:12px;border-bottom:1px solid #1e1e1e;margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.brand-dot{display:inline-block;width:7px;height:7px;background:#00d4aa;border-radius:50%;flex-shrink:0;}

.snav-sec{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:#2a2a2a!important;margin:14px 0 4px 2px;}
.sstat{padding:5px 2px;border-bottom:1px solid #191919;}
.sstat-l{font-size:10px;color:#333!important;text-transform:uppercase;letter-spacing:.05em;}
.sstat-v{font-size:12px;font-weight:600;color:#9ca3af!important;margin-top:1px;}

/* KPI Cards */
.kpi{background:#161616;border:1px solid #1e1e1e;border-radius:10px;padding:.9rem 1.1rem;}
.kpi-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#4b5563;margin-bottom:4px;}
.kpi-trend-pos{font-size:12px;font-weight:700;color:#00d4aa;margin-bottom:2px;letter-spacing:.01em;}
.kpi-trend-neg{font-size:12px;font-weight:700;color:#ef4444;margin-bottom:2px;letter-spacing:.01em;}
.kpi-trend-neu{font-size:12px;font-weight:600;color:#6b7280;margin-bottom:2px;}
.kpi-value{font-size:40px;font-weight:800;color:#ffffff;line-height:1;letter-spacing:-2px;margin-bottom:4px;}
.kpi-sub{font-size:11px;color:#374151;font-weight:400;border-top:1px solid #1e1e1e;padding-top:6px;margin-top:2px;}

/* Chart cards */
.cc{background:#161616;border:1px solid #1e1e1e;border-radius:10px;padding:1rem 1.2rem 0;margin-top:.6rem;}
.cc-title{font-size:14px;font-weight:600;color:#ffffff;margin-bottom:.2rem;}
.cc-sub{font-size:12px;color:#4b5563;margin-bottom:.5rem;}

/* Page header */
.ph{font-size:38px;font-weight:800;color:#ffffff;letter-spacing:-1.5px;margin:0;line-height:1.1;}
.psub{font-size:13px;color:#6b7280;margin-bottom:.8rem;margin-top:4px;font-weight:400;letter-spacing:.01em;line-height:1.5;max-width:860px;}

/* Badges */
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;margin:2px;}
.pos{background:#052e16;color:#00d4aa;}
.neg{background:#1c0a0a;color:#ef4444;}
.p0{background:#1c0a0a;color:#ef4444;font-weight:700;}
.p1{background:#1c1200;color:#f59e0b;}
.p2{background:#052e16;color:#00d4aa;}
.eng{background:#0c1a3a;color:#60a5fa;}
.prd{background:#1a0c3a;color:#a78bfa;}
.des{background:#2d0a1e;color:#f472b6;}

/* Action/insight rows */
.arow{background:#1a1a1a;border:1px solid #1e1e1e;border-radius:6px;padding:10px 14px;margin:5px 0;font-size:13px;color:#9ca3af;}
.prow{border-left:2px solid #ef4444;background:#120808;border-radius:0 6px 6px 0;padding:9px 13px;margin:5px 0;font-size:13px;color:#9ca3af;}
.drow{border-left:2px solid #00d4aa;background:#081210;border-radius:0 6px 6px 0;padding:9px 13px;margin:5px 0;font-size:13px;color:#9ca3af;}
.srow{background:#1a1a1a;border:1px solid #1e1e1e;border-radius:6px;padding:10px 14px;margin:5px 0;font-size:13px;color:#9ca3af;}

/* Insight box */
.insight{background:#0f1a16;border:1px solid #1e3a2e;border-left:3px solid #00d4aa;border-radius:0 8px 8px 0;padding:14px 18px;margin:12px 0;font-size:13px;color:#9ca3af;line-height:1.7;}
.insight-lbl{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#00d4aa;margin-bottom:6px;}
</style>
""", unsafe_allow_html=True)

BG = "#161616"
PLOT_BG = "#161616"
PAPER_BG = "#161616"
GRID_COLOR = "#1e1e1e"
FONT_COLOR = "#6b7280"
CYAN = "#00d4aa"
RED = "#ef4444"
AMBER = "#f59e0b"
BLUE = "#60a5fa"
PURPLE = "#a78bfa"
PINK = "#f472b6"
FONT = dict(family="Inter", size=11, color=FONT_COLOR)


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


def kpi(label, value, trend, trend_class, sub):
    return f'''<div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="{trend_class}">{trend}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>'''


# SIDEBAR
with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-dot"></span>VoC Intelligence</div>', unsafe_allow_html=True)
    page = st.radio("", ["Daily Brief","App Deep Dive","Action Board","Full Data"], label_visibility="collapsed")
    st.markdown('<hr style="border:none;border-top:1px solid #1e1e1e;margin:12px 0;">', unsafe_allow_html=True)

    st.markdown('<div class="snav-sec">Dataset</div>', unsafe_allow_html=True)
    for l,v in [("Reviews","200,000"),("Apps","20"),("Bundles",str(total)),("Actions flagged",str(ta))]:
        st.markdown(f'<div class="sstat"><div class="sstat-l">{l}</div><div class="sstat-v">{v}</div></div>', unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid #1e1e1e;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown('<div class="snav-sec">Model</div>', unsafe_allow_html=True)
    for l,v in [("Architecture","FLAN-T5 + LoRA"),("Checkpoint","3,449 steps"),("Hardware","Tesla T4 GPU"),("Accuracy","85.74%")]:
        st.markdown(f'<div class="sstat"><div class="sstat-l">{l}</div><div class="sstat-v">{v}</div></div>', unsafe_allow_html=True)

    st.markdown('<br><p style="font-size:10px;color:#1e1e1e;text-align:center;margin-top:2rem">Tanushree Poojary · UIUC 2026</p>', unsafe_allow_html=True)


# PAGE 1 — DAILY BRIEF
if page == "Daily Brief":
    st.markdown('<div class="ph">VoC Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">AI-powered Voice of Customer analytics across 200,000 Google Play reviews. Surfacing user sentiment, critical pain points, and prioritized product actions to drive faster, evidence-based decisions.</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("Reviews Analyzed","200K","↑ 100 bundles processed","kpi-trend-pos","Google Play · 20 apps"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Positive Sentiment",str(pos),f"↑ +{round(pos/total*100)}% of all bundles","kpi-trend-pos","Users satisfied"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Negative Sentiment",str(neg),f"↓ -{round(neg/total*100)}% needs attention","kpi-trend-neg","Users dissatisfied"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Critical P0 Issues",str(p0c),"↓ -2.1% Fix immediately","kpi-trend-neg","Before next release"), unsafe_allow_html=True)

    st.write("")
    st.markdown('''<div class="insight">
        <div class="insight-lbl">AI Insight</div>
        Sentiment is evenly split: 50% positive, 50% negative. Engineering owns 54% of all recommended actions,
        suggesting product quality and stability issues drive dissatisfaction more than design gaps.
        3 P0 critical issues require immediate resolution before the next product release.
    </div>''', unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown('<div class="cc"><div class="cc-title">Sentiment by App</div><div class="cc-sub">Negative vs positive breakdown across all 20 apps</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app","sentiment"]).size().reset_index(name="count")
        fig = px.bar(app_sent, x="app", y="count", color="sentiment",
                     color_discrete_map={"positive":CYAN,"negative":RED},
                     barmode="group", height=340)
        fig.update_layout(
            margin=dict(l=40,r=10,t=10,b=140),
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=FONT,
            legend=dict(orientation="h",y=-0.5,x=0.3,bgcolor="rgba(0,0,0,0)",
                        font=dict(color=FONT_COLOR),title_text=""),
            xaxis=dict(showgrid=False,tickangle=-45,title="",
                       tickfont=dict(color=FONT_COLOR,size=10),
                       linecolor=GRID_COLOR),
            yaxis=dict(showgrid=True,gridcolor=GRID_COLOR,
                       tickfont=dict(color=FONT_COLOR),
                       title=dict(text="Count",font=dict(color=FONT_COLOR,size=11)))
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="cc"><div class="cc-title">Cumulative Sentiment Trend</div><div class="cc-sub">Running total across 100 bundles</div>', unsafe_allow_html=True)
        trend = df.sort_values("sample_id").copy()
        trend["Positive"] = (trend["sentiment"]=="positive").cumsum()
        trend["Negative"] = (trend["sentiment"]=="negative").cumsum()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=trend["sample_id"], y=trend["Positive"], name="Positive",
            line=dict(color=CYAN,width=2.5), mode="lines",
            fill="tozeroy", fillcolor="rgba(0,212,170,0.08)"
        ))
        fig2.add_trace(go.Scatter(
            x=trend["sample_id"], y=trend["Negative"], name="Negative",
            line=dict(color=RED,width=2.5), mode="lines",
            fill="tozeroy", fillcolor="rgba(239,68,68,0.08)"
        ))
        fig2.update_layout(
            height=300, margin=dict(l=40,r=10,t=10,b=60),
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG, font=FONT,
            legend=dict(orientation="h",y=-0.25,x=0,bgcolor="rgba(0,0,0,0)",
                        font=dict(color=FONT_COLOR)),
            xaxis=dict(showgrid=False,linecolor=GRID_COLOR,
                       tickfont=dict(color=FONT_COLOR),
                       title=dict(text="Bundle ID",font=dict(color=FONT_COLOR,size=11))),
            yaxis=dict(showgrid=True,gridcolor=GRID_COLOR,
                       tickfont=dict(color=FONT_COLOR),
                       title=dict(text="Count",font=dict(color=FONT_COLOR,size=11)))
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom row — 3 charts horizontal
    st.write("")
    b1, b2, b3 = st.columns(3)

    with b1:
        st.markdown('<div class="cc"><div class="cc-title">Sentiment Split</div><div class="cc-sub">Overall distribution</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=["Positive","Negative"], values=[pos,neg],
            marker=dict(colors=[CYAN,RED], line=dict(color=PLOT_BG,width=3)),
            hole=0.6, textinfo="percent",
            textfont=dict(family="Inter",size=12,color="#fff"),
            hovertemplate="%{label}: %{value}<extra></extra>"
        ))
        fig3.add_annotation(
            text=f"<b>{round(pos/total*100)}%</b><br>positive",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="Inter",size=13,color="#fff")
        )
        fig3.update_layout(
            height=220, margin=dict(l=10,r=10,t=10,b=40),
            paper_bgcolor=PAPER_BG, showlegend=True,
            legend=dict(orientation="h",x=0.1,y=-0.1,
                        font=dict(color=FONT_COLOR,size=11)),
            font=dict(family="Inter")
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="cc"><div class="cc-title">Action Owners</div><div class="cc-sub">Who owns the fixes</div>', unsafe_allow_html=True)
        if len(af):
            oc = af["owner"].value_counts().reset_index()
            oc.columns = ["owner","count"]
            fig4 = px.bar(oc, x="count", y="owner", orientation="h",
                          color="owner",
                          color_discrete_map={"Engineering":BLUE,"Product":PURPLE,"Design":PINK},
                          height=220, text="count")
            fig4.update_traces(textfont=dict(color="#fff",size=12), textposition="inside")
            fig4.update_layout(
                margin=dict(l=10,r=10,t=5,b=10),
                plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
                showlegend=False, font=FONT,
                xaxis=dict(showgrid=True,gridcolor=GRID_COLOR,
                           tickfont=dict(color=FONT_COLOR),title=""),
                yaxis=dict(showgrid=False,tickfont=dict(color=FONT_COLOR),title="")
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with b3:
        st.markdown('<div class="cc"><div class="cc-title">Priority Breakdown</div><div class="cc-sub">P0 · P1 · P2 distribution</div>', unsafe_allow_html=True)
        if len(af):
            pc = af["priority"].value_counts().reset_index()
            pc.columns = ["priority","count"]
            fig5 = px.bar(pc, x="priority", y="count",
                          color="priority",
                          color_discrete_map={"P0":RED,"P1":AMBER,"P2":CYAN},
                          height=220, text="count")
            fig5.update_traces(textfont=dict(color="#fff",size=13,family="Inter"),
                               textposition="inside")
            fig5.update_layout(
                margin=dict(l=10,r=10,t=5,b=10),
                plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
                showlegend=False, font=FONT,
                xaxis=dict(showgrid=False,tickfont=dict(color=FONT_COLOR,size=12),title=""),
                yaxis=dict(showgrid=False,visible=False)
            )
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)


# PAGE 2 — APP DEEP DIVE
elif page == "App Deep Dive":
    st.markdown('<div class="ph">App Deep Dive</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Select any of the 20 apps to explore user pain points, product delighters, AI-generated summaries, and prioritized engineering and product actions.</div>', unsafe_allow_html=True)

    sel = st.selectbox("", apps, label_visibility="collapsed")
    adf = df[df["app"]==sel]
    aacts = [a for _,row in adf.iterrows() for a in row["suggested_actions"]]
    pp = round((adf["sentiment"]=="positive").mean()*100)
    p0a = sum(1 for a in aacts if a.get("priority")=="P0")
    p1a = sum(1 for a in aacts if a.get("priority")=="P1")

    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("Bundles",str(len(adf)),"","kpi-trend-neu",f"for {sel}"), unsafe_allow_html=True)
    with c2:
        tc = "kpi-trend-pos" if pp>=50 else "kpi-trend-neg"
        ti = "↑" if pp>=50 else "↓"
        st.markdown(kpi("Positive Sentiment",f"{pp}%",f"{ti} {'Good signal' if pp>=50 else 'Needs attention'}",tc,""), unsafe_allow_html=True)
    with c3: st.markdown(kpi("P0 Critical",str(p0a),"↓ Fix immediately","kpi-trend-neg",""), unsafe_allow_html=True)
    with c4: st.markdown(kpi("P1 Sprint",str(p1a),"Address this sprint","kpi-trend-neu",""), unsafe_allow_html=True)

    st.write("")
    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="cc"><div class="cc-title">Pain Points</div><div class="cc-sub">What users are frustrated about</div>', unsafe_allow_html=True)
        pains = [p for _,row in adf.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"],list) else []) if isinstance(p,str) and len(p)>10]
        for p in pains[:6]: st.markdown(f'<div class="prow">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains: st.caption("No pain points detected")
        st.markdown('<br><div class="cc-title" style="color:#fff">Delighters</div><div class="cc-sub">What users love</div>', unsafe_allow_html=True)
        dels = [d for _,row in adf.iterrows() for d in (row["delighters"] if isinstance(row["delighters"],list) else []) if isinstance(d,str) and len(d)>10]
        for d in dels[:6]: st.markdown(f'<div class="drow">{d[:160]}</div>', unsafe_allow_html=True)
        if not dels: st.caption("No delighters detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="cc"><div class="cc-title">Recommended Actions</div><div class="cc-sub">Prioritized for product team</div>', unsafe_allow_html=True)
        if aacts:
            for a in aacts:
                oc2={"Engineering":"eng","Product":"prd","Design":"des"}.get(a.get("owner",""),"eng")
                pc2={"P0":"p0","P1":"p1","P2":"p2"}.get(a.get("priority",""),"p1")
                st.markdown(f'<div class="arow"><span class="badge {pc2}">{a.get("priority","")}</span> <span class="badge {oc2}">{a.get("owner","")}</span> {a.get("action","")}</div>', unsafe_allow_html=True)
        else: st.caption("No actions flagged")
        st.markdown('<br><div class="cc-title" style="color:#fff">AI Summaries</div><div class="cc-sub">Generated from review bundles</div>', unsafe_allow_html=True)
        for _,row in adf.head(6).iterrows():
            bc="pos" if row["sentiment"]=="positive" else "neg"
            st.markdown(f'<div class="srow"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# PAGE 3 — ACTION BOARD
elif page == "Action Board":
    st.markdown('<div class="ph">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">35 AI-generated product actions ranked by severity. Filter by priority level and team ownership to build your sprint backlog and align engineering, product, and design teams.</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2 = st.columns(2)
    with f1: pf=st.multiselect("Priority",["P0","P1","P2"],default=["P0","P1","P2"])
    with f2: of=st.multiselect("Owner",["Engineering","Product","Design"],default=["Engineering","Product","Design"])

    filt=af.copy()
    if pf: filt=filt[filt["priority"].isin(pf)]
    if of: filt=filt[filt["owner"].isin(of)]

    st.write("")
    c1,c2,c3 = st.columns(3)
    p0f=int((filt["priority"]=="P0").sum()) if len(filt) else 0
    engf=int((filt["owner"]=="Engineering").sum()) if len(filt) else 0
    with c1: st.markdown(kpi("Total Actions",str(len(filt)),"","kpi-trend-neu","in current filter"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("P0 Critical",str(p0f),"↓ Fix before shipping","kpi-trend-neg",""), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Engineering",str(engf),"↑ items assigned","kpi-trend-pos",""), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="cc"><div class="cc-title">All Actions</div><div class="cc-sub">Sorted by priority</div>', unsafe_allow_html=True)
    if len(filt):
        for _,row in filt.sort_values("priority").iterrows():
            oc2={"Engineering":"eng","Product":"prd","Design":"des"}.get(row["owner"],"eng")
            pc2={"P0":"p0","P1":"p1","P2":"p2"}.get(row["priority"],"p1")
            st.markdown(f'<div class="arow"><span class="badge {pc2}">{row["priority"]}</span> <span class="badge {oc2}">{row["owner"]}</span> {row["action"]}</div>', unsafe_allow_html=True)
    else: st.caption("No actions match filters")
    st.markdown('</div>', unsafe_allow_html=True)


# PAGE 4 — FULL DATA
elif page == "Full Data":
    st.markdown('<div class="ph">Full Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Complete results from 100 AI-processed review bundles across 20 apps. Filter by sentiment or app, explore raw AI summaries, and export structured data for further analysis.</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2=st.columns(2)
    with f1: sf=st.multiselect("Sentiment",["positive","negative"],default=["positive","negative"])
    with f2: appf=st.multiselect("App",apps,default=[])

    rdf=df.copy()
    if sf: rdf=rdf[rdf["sentiment"].isin(sf)]
    if appf: rdf=rdf[rdf["app"].isin(appf)]

    st.write("")
    c1,c2,c3=st.columns(3)
    with c1: st.markdown(kpi("Showing",str(len(rdf)),"","kpi-trend-neu","of 100 bundles"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Positive",str((rdf["sentiment"]=="positive").sum()),"","kpi-trend-pos","in selection"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Negative",str((rdf["sentiment"]=="negative").sum()),"","kpi-trend-neg","in selection"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="cc"><div class="cc-title">Results</div><div class="cc-sub">All processed review bundles</div>', unsafe_allow_html=True)
    disp=rdf[["app","sentiment","summary"]].copy()
    disp.columns=["App","Sentiment","AI Summary"]
    st.dataframe(disp,use_container_width=True,height=460,hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    st.download_button("Download CSV",df.to_csv(index=False),"voc_results.csv","text/csv")
