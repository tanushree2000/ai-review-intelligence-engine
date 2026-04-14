import streamlit as st
import pandas as pd
import ast
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="VoC Intelligence Engine", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;}

/* Mint background on main */
.main{background:#dff0ec;}
.main .block-container{background:#dff0ec;padding:1.8rem 2.2rem;max-width:100%;}

/* Dark narrow sidebar */
section[data-testid="stSidebar"]{background:#1a1f2e!important;min-width:200px!important;max-width:200px!important;}
section[data-testid="stSidebar"]>div{padding:1.5rem 1rem;}
section[data-testid="stSidebar"] *{color:#8892a4!important;}

.brand-wrap{display:flex;align-items:center;gap:10px;padding-bottom:16px;border-bottom:1px solid #252b3b;margin-bottom:16px;}
.brand-logo{width:36px;height:36px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:#1a1f2e;}
.brand-name{font-size:15px;font-weight:700;color:#fff!important;}
.snav-sec{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#3a4459!important;margin:16px 0 6px 2px;}
.sinfo{background:#12172a;border-radius:6px;padding:8px 10px;margin-bottom:5px;}
.sinfo-l{font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:#3a4459!important;}
.sinfo-v{font-size:14px;font-weight:600;color:#c8d0dc!important;margin-top:1px;}

/* White content area */
.content-wrap{background:#fff;border-radius:12px;padding:1.5rem 1.8rem;margin-bottom:1rem;}

/* KPI Cards — dark header style */
.kpi{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.kpi-head{background:#1a1f2e;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;}
.kpi-head-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#8892a4;}
.kpi-body{padding:14px 16px 12px;display:flex;justify-content:space-between;align-items:flex-end;}
.kpi-left{}
.kpi-val{font-size:32px;font-weight:800;color:#1a1f2e;line-height:1;margin-bottom:5px;}
.kpi-trend{font-size:11px;font-weight:500;}
.kpi-trend-g{color:#2ecc9a;}
.kpi-trend-r{color:#e8634a;}
.kpi-trend-gr{color:#8892a4;}
.kpi-icon{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;}
.icon-coral{background:#e8634a;}
.icon-green{background:#2ecc9a;}
.icon-dark{background:#252b3b;}
.icon-mint{background:#dff0ec;}

/* Chart cards */
.chart-card{background:#fff;border-radius:10px;padding:1.2rem 1.4rem;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.chart-card-dark{background:#1a1f2e;border-radius:10px;padding:1.2rem 1.4rem;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.chart-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#8892a4;margin-bottom:.8rem;}
.chart-title-light{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#3a4459;margin-bottom:.8rem;}

/* Page */
.page-title{font-size:20px;font-weight:800;color:#1a1f2e;margin:0;text-transform:uppercase;letter-spacing:.05em;}
.breadcrumb{font-size:11px;color:#8892a4;margin-bottom:1.4rem;}

/* Badges */
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;margin:2px;}
.pos{background:#d1fae5;color:#065f46;}
.neg{background:#fee2e2;color:#991b1b;}
.p0{background:#fee2e2;color:#991b1b;}
.p1{background:#fef3c7;color:#92400e;}
.p2{background:#d1fae5;color:#065f46;}
.eng{background:#dbeafe;color:#1e40af;}
.prd{background:#ede9fe;color:#5b21b6;}
.des{background:#fce7f3;color:#9d174d;}

.arow{background:#f8fafc;border:1px solid #e8edf2;border-radius:6px;padding:8px 12px;margin:4px 0;font-size:13px;color:#334155;}
.prow{border-left:3px solid #e8634a;background:#fff8f6;border-radius:0 6px 6px 0;padding:7px 11px;margin:4px 0;font-size:13px;color:#374151;}
.drow{border-left:3px solid #2ecc9a;background:#f0fdf8;border-radius:0 6px 6px 0;padding:7px 11px;margin:4px 0;font-size:13px;color:#374151;}
.srow{background:#f8fafc;border:1px solid #e8edf2;border-radius:6px;padding:8px 12px;margin:4px 0;font-size:13px;color:#334155;}
</style>
""", unsafe_allow_html=True)


def svg_icon(name, color="#fff"):
    icons = {
        "trending": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "users": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>',
        "bar": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round"><rect x="3" y="12" width="4" height="9"/><rect x="10" y="5" width="4" height="16"/><rect x="17" y="9" width="4" height="12"/></svg>',
        "alert": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "dollar": f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
    }
    return icons.get(name, icons["bar"])


def kpi_card(label, value, trend, trend_class, icon_name, icon_bg):
    return f'''<div class="kpi">
        <div class="kpi-head">
            <span class="kpi-head-label">{label}</span>
        </div>
        <div class="kpi-body">
            <div class="kpi-left">
                <div class="kpi-val">{value}</div>
                <div class="kpi-trend {trend_class}">{trend}</div>
            </div>
            <div class="kpi-icon {icon_bg}">{svg_icon(icon_name)}</div>
        </div>
    </div>'''


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
ta = len(af)
apps = sorted(df["app"].unique().tolist())

PLOT_BG = "#fff"
FONT = "Inter"
GREEN = "#2ecc9a"
CORAL = "#e8634a"
DARK = "#1a1f2e"
MINT = "#dff0ec"

# SIDEBAR
with st.sidebar:
    st.markdown(f'''<div class="brand-wrap">
        <div class="brand-logo">V</div>
        <div class="brand-name">VoC Engine</div>
    </div>''', unsafe_allow_html=True)

    page = st.radio("", ["Dashboard","App Explorer","Action Board","Full Results"], label_visibility="collapsed")

    st.markdown('<div class="snav-sec">Dataset</div>', unsafe_allow_html=True)
    for l,v in [("Reviews","200,000"),("Apps","20"),("Bundles",str(total)),("Actions",str(ta))]:
        st.markdown(f'<div class="sinfo"><div class="sinfo-l">{l}</div><div class="sinfo-v">{v}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="snav-sec">Model</div>', unsafe_allow_html=True)
    for l,v in [("Architecture","FLAN-T5 + LoRA"),("Steps","3,449"),("GPU","Tesla T4"),("Accuracy","85.74%")]:
        st.markdown(f'<div class="sinfo"><div class="sinfo-l">{l}</div><div class="sinfo-v">{v}</div></div>', unsafe_allow_html=True)

    st.markdown('<br><p style="font-size:10px;color:#252b3b;text-align:center">Tanushree Poojary · UIUC 2026</p>', unsafe_allow_html=True)


if page == "Dashboard":
    st.markdown('<div class="page-title">Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Dashboard</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Total Reviews","200K","+100 bundles processed","kpi-trend-g","trending","icon-coral"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Positive Sentiment",str(pos),f"+{round(pos/total*100)}% of all bundles","kpi-trend-g","users","icon-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Negative Sentiment",str(neg),f"-{round(neg/total*100)}% needs attention","kpi-trend-r","alert","icon-coral"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Actions Flagged",str(ta),f"{p0c} critical P0 issues","kpi-trend-r","bar","icon-dark"), unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown('<div class="chart-card"><div class="chart-title">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app","sentiment"]).size().reset_index(name="count")
        fig = px.bar(app_sent, x="app", y="count", color="sentiment",
                     color_discrete_map={"positive": GREEN, "negative": CORAL},
                     barmode="group", height=260)
        fig.update_layout(
            margin=dict(l=0,r=0,t=0,b=70),
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family=FONT, size=11, color="#64748b"),
            legend=dict(orientation="h", y=-0.35, x=0, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, tickangle=-40, title=""),
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card-dark"><div class="chart-title-light">Cumulative trend</div>', unsafe_allow_html=True)
        trend = df.sort_values("sample_id").copy()
        trend["Positive"] = (trend["sentiment"]=="positive").cumsum()
        trend["Negative"] = (trend["sentiment"]=="negative").cumsum()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=trend["sample_id"], y=trend["Positive"], name="Positive",
            line=dict(color=GREEN, width=2.5), mode="lines+markers",
            marker=dict(size=4, color=GREEN),
            fill="tozeroy", fillcolor="rgba(46,204,154,0.12)"))
        fig2.add_trace(go.Scatter(x=trend["sample_id"], y=trend["Negative"], name="Negative",
            line=dict(color=CORAL, width=2.5), mode="lines+markers",
            marker=dict(size=4, color=CORAL),
            fill="tozeroy", fillcolor="rgba(232,99,74,0.12)"))
        fig2.update_layout(
            height=180, margin=dict(l=0,r=0,t=0,b=30),
            plot_bgcolor=DARK, paper_bgcolor=DARK,
            font=dict(family=FONT, size=11, color="#8892a4"),
            legend=dict(orientation="h", y=-0.35, bgcolor="rgba(0,0,0,0)", font=dict(color="#8892a4")),
            xaxis=dict(showgrid=False, color="#3a4459"),
            yaxis=dict(showgrid=True, gridcolor="#252b3b", color="#3a4459")
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-card"><div class="chart-title">Sentiment split</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=["Positive","Negative"], values=[pos,neg],
            marker=dict(colors=[GREEN, CORAL]),
            hole=0.6, textinfo="percent+label",
            textfont=dict(family=FONT, size=12, color=DARK),
            hovertemplate="%{label}: %{value}<extra></extra>"
        ))
        fig3.update_layout(
            height=220, margin=dict(l=0,r=0,t=10,b=10),
            paper_bgcolor=PLOT_BG, showlegend=False,
            font=dict(family=FONT)
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card-dark"><div class="chart-title-light">Action owners</div>', unsafe_allow_html=True)
        if len(af):
            oc = af["owner"].value_counts().reset_index()
            oc.columns = ["owner","count"]
            colors = {"Engineering":"#2563eb","Product":"#7c3aed","Design":"#db2777"}
            fig4 = px.bar(oc, x="count", y="owner", orientation="h",
                          color="owner", color_discrete_map=colors, height=150)
            fig4.update_layout(
                margin=dict(l=0,r=0,t=0,b=0),
                plot_bgcolor=DARK, paper_bgcolor=DARK,
                showlegend=False, font=dict(family=FONT,size=11,color="#8892a4"),
                xaxis=dict(showgrid=True,gridcolor="#252b3b",color="#3a4459"),
                yaxis=dict(showgrid=False,color="#8892a4")
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card"><div class="chart-title">Priority breakdown</div>', unsafe_allow_html=True)
        if len(af):
            pc = af["priority"].value_counts().reset_index()
            pc.columns = ["priority","count"]
            fig5 = px.bar(pc, x="priority", y="count",
                          color="priority",
                          color_discrete_map={"P0":CORAL,"P1":"#f59e0b","P2":GREEN},
                          height=150)
            fig5.update_layout(
                margin=dict(l=0,r=0,t=0,b=0),
                plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
                showlegend=False, font=dict(family=FONT,size=11,color="#64748b"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True,gridcolor="#f1f5f9")
            )
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "App Explorer":
    st.markdown('<div class="page-title">App Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; App Explorer</div>', unsafe_allow_html=True)

    sel = st.selectbox("Select an app", apps)
    adf = df[df["app"]==sel]
    aacts = [a for _, row in adf.iterrows() for a in row["suggested_actions"]]
    pp = round((adf["sentiment"]=="positive").mean()*100)
    p0a = sum(1 for a in aacts if a.get("priority")=="P0")
    p1a = sum(1 for a in aacts if a.get("priority")=="P1")

    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Bundles",str(len(adf)),"reviewed","kpi-trend-gr","bar","icon-dark"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Positive",f"{pp}%","Good signal" if pp>=50 else "Low","kpi-trend-g" if pp>=50 else "kpi-trend-r","trending","icon-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("P0 Critical",str(p0a),"Fix immediately","kpi-trend-r","alert","icon-coral"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("P1 Sprint",str(p1a),"Address soon","kpi-trend-r","bar","icon-dark"), unsafe_allow_html=True)

    st.write("")
    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="chart-card"><div class="chart-title">Pain points</div>', unsafe_allow_html=True)
        pains = [p for _,row in adf.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"],list) else []) if isinstance(p,str) and len(p)>10]
        for p in pains[:5]: st.markdown(f'<div class="prow">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains: st.caption("None detected")
        st.markdown('<br><div class="chart-title">Delighters</div>', unsafe_allow_html=True)
        dels = [d for _,row in adf.iterrows() for d in (row["delighters"] if isinstance(row["delighters"],list) else []) if isinstance(d,str) and len(d)>10]
        for d in dels[:5]: st.markdown(f'<div class="drow">{d[:160]}</div>', unsafe_allow_html=True)
        if not dels: st.caption("None detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-card"><div class="chart-title">Recommended actions</div>', unsafe_allow_html=True)
        if aacts:
            for a in aacts:
                oc2={"Engineering":"eng","Product":"prd","Design":"des"}.get(a.get("owner",""),"eng")
                pc2={"P0":"p0","P1":"p1","P2":"p2"}.get(a.get("priority",""),"p1")
                st.markdown(f'<div class="arow"><span class="badge {pc2}">{a.get("priority","")}</span> <span class="badge {oc2}">{a.get("owner","")}</span> {a.get("action","")}</div>', unsafe_allow_html=True)
        else: st.caption("No actions flagged")
        st.markdown('<br><div class="chart-title">AI summaries</div>', unsafe_allow_html=True)
        for _,row in adf.head(5).iterrows():
            bc="pos" if row["sentiment"]=="positive" else "neg"
            st.markdown(f'<div class="srow"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "Action Board":
    st.markdown('<div class="page-title">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Action Board</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2 = st.columns(2)
    with f1: pf=st.multiselect("Priority",["P0","P1","P2"],default=["P0","P1","P2"])
    with f2: of=st.multiselect("Owner",["Engineering","Product","Design"],default=["Engineering","Product","Design"])

    filt=af.copy()
    if pf: filt=filt[filt["priority"].isin(pf)]
    if of: filt=filt[filt["owner"].isin(of)]

    st.write("")
    c1,c2,c3=st.columns(3)
    p0f=int((filt["priority"]=="P0").sum()) if len(filt) else 0
    engf=int((filt["owner"]=="Engineering").sum()) if len(filt) else 0
    with c1: st.markdown(kpi_card("Total Actions",str(len(filt)),"filtered results","kpi-trend-gr","bar","icon-dark"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("P0 Critical",str(p0f),"Fix immediately","kpi-trend-r","alert","icon-coral"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Engineering",str(engf),"actions assigned","kpi-trend-gr","users","icon-green"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="chart-card"><div class="chart-title">All actions</div>', unsafe_allow_html=True)
    if len(filt):
        for _,row in filt.sort_values("priority").iterrows():
            oc2={"Engineering":"eng","Product":"prd","Design":"des"}.get(row["owner"],"eng")
            pc2={"P0":"p0","P1":"p1","P2":"p2"}.get(row["priority"],"p1")
            st.markdown(f'<div class="arow"><span class="badge {pc2}">{row["priority"]}</span> <span class="badge {oc2}">{row["owner"]}</span> {row["action"]}</div>', unsafe_allow_html=True)
    else: st.caption("No actions match filters")
    st.markdown('</div>', unsafe_allow_html=True)


elif page == "Full Results":
    st.markdown('<div class="page-title">Full Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Full Results</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2=st.columns(2)
    with f1: sf=st.multiselect("Sentiment",["positive","negative"],default=["positive","negative"])
    with f2: appf=st.multiselect("App",apps,default=[])

    rdf=df.copy()
    if sf: rdf=rdf[rdf["sentiment"].isin(sf)]
    if appf: rdf=rdf[rdf["app"].isin(appf)]

    c1,c2,c3=st.columns(3)
    with c1: st.markdown(kpi_card("Showing",str(len(rdf)),"bundles","kpi-trend-gr","bar","icon-dark"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Positive",str((rdf["sentiment"]=="positive").sum()),"bundles","kpi-trend-g","trending","icon-green"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Negative",str((rdf["sentiment"]=="negative").sum()),"bundles","kpi-trend-r","alert","icon-coral"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="chart-card"><div class="chart-title">Results</div>', unsafe_allow_html=True)
    disp=rdf[["app","sentiment","summary"]].copy()
    disp.columns=["App","Sentiment","AI Summary"]
    st.dataframe(disp,use_container_width=True,height=460,hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    st.download_button("Download CSV",df.to_csv(index=False),"voc_results.csv","text/csv")
