import streamlit as st
import pandas as pd
import ast
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="VoC Intelligence Engine", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.main .block-container{padding:1.5rem 2rem;background:#f0f2f6;max-width:100%;}

section[data-testid="stSidebar"]{background:#1e2a3a!important;min-width:230px!important;max-width:230px!important;}
section[data-testid="stSidebar"]>div{padding:1.2rem 1rem;}
section[data-testid="stSidebar"] *{color:#8fa3b8!important;}

.brand{font-size:17px;font-weight:700;color:#fff!important;letter-spacing:.3px;padding-bottom:14px;border-bottom:1px solid #2e3e50;margin-bottom:14px;display:block;}
.snav-lbl{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#4a6278!important;margin:14px 0 6px 4px;display:block;}
.sinfo{background:#162030;border-radius:6px;padding:9px 11px;margin-bottom:6px;}
.sinfo-lbl{font-size:10px;color:#4a6278!important;text-transform:uppercase;letter-spacing:.06em;}
.sinfo-val{font-size:15px;font-weight:600;color:#e2e8f0!important;margin-top:1px;}

/* Bootstrap-style metric cards */
.kcard{background:#fff;border-radius:6px;overflow:hidden;border:none;margin-bottom:4px;}
.kcard-header{padding:10px 16px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#fff;}
.kcard-body{padding:14px 16px 12px;}
.kcard-val{font-size:34px;font-weight:700;line-height:1;margin-bottom:4px;}
.kcard-sub{font-size:12px;font-weight:400;}
.h-blue{background:#2563eb;}
.h-green{background:#059669;}
.h-red{background:#dc2626;}
.h-orange{background:#d97706;}
.h-purple{background:#7c3aed;}
.h-dark{background:#1e2a3a;}
.v-blue{color:#2563eb;}
.v-green{color:#059669;}
.v-red{color:#dc2626;}
.v-orange{color:#d97706;}
.v-purple{color:#7c3aed;}
.v-dark{color:#1e2a3a;}
.s-blue{color:#93c5fd;}
.s-green{color:#6ee7b7;}
.s-red{color:#fca5a5;}
.s-orange{color:#fcd34d;}

/* Chart card */
.ccard{background:#fff;border-radius:6px;padding:1.1rem 1.3rem;margin-top:.8rem;border-top:3px solid #2563eb;}
.ccard-green{background:#fff;border-radius:6px;padding:1.1rem 1.3rem;margin-top:.8rem;border-top:3px solid #059669;}
.ccard-red{background:#fff;border-radius:6px;padding:1.1rem 1.3rem;margin-top:.8rem;border-top:3px solid #dc2626;}
.ccard-orange{background:#fff;border-radius:6px;padding:1.1rem 1.3rem;margin-top:.8rem;border-top:3px solid #d97706;}
.ccard-purple{background:#fff;border-radius:6px;padding:1.1rem 1.3rem;margin-top:.8rem;border-top:3px solid #7c3aed;}
.ccard-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#64748b;margin-bottom:.8rem;}

.page-hdr{font-size:20px;font-weight:700;color:#1e293b;margin:0 0 2px;}
.breadcrumb{font-size:12px;color:#94a3b8;margin-bottom:1.2rem;}

.badge{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:600;margin:2px;}
.pos{background:#d1fae5;color:#065f46;}
.neg{background:#fee2e2;color:#991b1b;}
.p0{background:#fee2e2;color:#991b1b;}
.p1{background:#fef3c7;color:#92400e;}
.p2{background:#d1fae5;color:#065f46;}
.eng{background:#dbeafe;color:#1e40af;}
.prd{background:#ede9fe;color:#5b21b6;}
.des{background:#fce7f3;color:#9d174d;}

.arow{background:#f8fafc;border:1px solid #e2e8f0;border-radius:5px;padding:8px 12px;margin:4px 0;font-size:13px;color:#334155;}
.prow{border-left:3px solid #ef4444;background:#fff5f5;border-radius:0 5px 5px 0;padding:7px 11px;margin:4px 0;font-size:13px;color:#374151;}
.drow{border-left:3px solid #10b981;background:#f0fdf4;border-radius:0 5px 5px 0;padding:7px 11px;margin:4px 0;font-size:13px;color:#374151;}
.srow{background:#f8fafc;border:1px solid #e2e8f0;border-radius:5px;padding:8px 12px;margin:4px 0;font-size:13px;color:#334155;}
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


def kcard(header_class, val_class, sub_class, label, value, sub):
    return f'''<div class="kcard">
        <div class="kcard-header {header_class}">{label}</div>
        <div class="kcard-body">
            <div class="kcard-val {val_class}">{value}</div>
            <div class="kcard-sub {sub_class}">{sub}</div>
        </div>
    </div>'''


# SIDEBAR
with st.sidebar:
    st.markdown('<span class="brand">VoC Intelligence</span>', unsafe_allow_html=True)
    page = st.radio("", ["Dashboard","App Explorer","Action Board","Full Results"], label_visibility="collapsed")
    st.markdown('<span class="snav-lbl">Dataset</span>', unsafe_allow_html=True)
    for lbl, val in [("Reviews","200,000"),("Apps","20"),("Bundles",str(total)),("Actions",str(ta))]:
        st.markdown(f'<div class="sinfo"><div class="sinfo-lbl">{lbl}</div><div class="sinfo-val">{val}</div></div>', unsafe_allow_html=True)
    st.markdown('<span class="snav-lbl">Model</span>', unsafe_allow_html=True)
    for lbl, val in [("Architecture","FLAN-T5 + LoRA"),("Steps","3,449"),("GPU","Tesla T4"),("Accuracy","85.74%")]:
        st.markdown(f'<div class="sinfo"><div class="sinfo-lbl">{lbl}</div><div class="sinfo-val">{val}</div></div>', unsafe_allow_html=True)
    st.markdown('<br><p style="font-size:10px;color:#2e3e50;text-align:center">Tanushree Poojary · UIUC 2026</p>', unsafe_allow_html=True)


if page == "Dashboard":
    st.markdown('<div class="page-hdr">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Dashboard</div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kcard("h-blue","v-blue","s-blue","Total Reviews","200K","Google Play Store"), unsafe_allow_html=True)
    with c2: st.markdown(kcard("h-green","v-green","s-green","Bundles Processed",str(total),"100 samples"), unsafe_allow_html=True)
    with c3: st.markdown(kcard("h-red","v-red","s-red","Negative Sentiment",str(neg),"50% — needs fix"), unsafe_allow_html=True)
    with c4: st.markdown(kcard("h-orange","v-orange","s-orange","Actions Flagged",str(ta),"Across all apps"), unsafe_allow_html=True)
    with c5: st.markdown(kcard("h-dark","v-dark","","Critical P0",str(p0c),"Fix immediately"), unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns([1.5,1])

    with col_l:
        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app","sentiment"]).size().reset_index(name="count")
        fig = px.bar(app_sent, x="app", y="count", color="sentiment",
                     color_discrete_map={"positive":"#059669","negative":"#dc2626"},
                     barmode="group", height=280)
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=60), plot_bgcolor="#fff", paper_bgcolor="#fff",
                          legend=dict(orientation="h",y=-0.25), xaxis_tickangle=-45,
                          font=dict(family="Inter",size=11), showlegend=True)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard-green"><div class="ccard-title">Cumulative sentiment trend</div>', unsafe_allow_html=True)
        trend = df.sort_values("sample_id").copy()
        trend["Positive"] = (trend["sentiment"]=="positive").cumsum()
        trend["Negative"] = (trend["sentiment"]=="negative").cumsum()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=trend["sample_id"], y=trend["Positive"], name="Positive", line=dict(color="#059669",width=2.5), fill="tozeroy", fillcolor="rgba(5,150,105,0.08)"))
        fig2.add_trace(go.Scatter(x=trend["sample_id"], y=trend["Negative"], name="Negative", line=dict(color="#dc2626",width=2.5), fill="tozeroy", fillcolor="rgba(220,38,38,0.08)"))
        fig2.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), plot_bgcolor="#fff", paper_bgcolor="#fff",
                           legend=dict(orientation="h",y=-0.3), font=dict(family="Inter",size=11))
        fig2.update_xaxes(showgrid=False, title="Bundle ID")
        fig2.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ccard-purple"><div class="ccard-title">Sentiment split</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=["Positive","Negative"], values=[pos,neg],
            marker=dict(colors=["#059669","#dc2626"]),
            hole=0.55, textinfo="percent+label",
            textfont=dict(family="Inter",size=12)
        ))
        fig3.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="#fff",
                           showlegend=False, font=dict(family="Inter"))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard-orange"><div class="ccard-title">Action owners</div>', unsafe_allow_html=True)
        if len(af):
            oc = af["owner"].value_counts().reset_index()
            oc.columns = ["owner","count"]
            fig4 = px.bar(oc, x="count", y="owner", orientation="h",
                          color="owner", color_discrete_sequence=["#2563eb","#7c3aed","#db2777"],
                          height=160)
            fig4.update_layout(margin=dict(l=0,r=0,t=0,b=0), plot_bgcolor="#fff", paper_bgcolor="#fff",
                               showlegend=False, font=dict(family="Inter",size=11))
            fig4.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
            fig4.update_yaxes(showgrid=False)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard-red"><div class="ccard-title">Priority distribution</div>', unsafe_allow_html=True)
        if len(af):
            pc = af["priority"].value_counts().reset_index()
            pc.columns = ["priority","count"]
            fig5 = px.bar(pc, x="priority", y="count",
                          color="priority", color_discrete_map={"P0":"#dc2626","P1":"#d97706","P2":"#059669"},
                          height=160)
            fig5.update_layout(margin=dict(l=0,r=0,t=0,b=0), plot_bgcolor="#fff", paper_bgcolor="#fff",
                               showlegend=False, font=dict(family="Inter",size=11))
            fig5.update_xaxes(showgrid=False)
            fig5.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "App Explorer":
    st.markdown('<div class="page-hdr">App Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; App Explorer</div>', unsafe_allow_html=True)

    sel = st.selectbox("Select an app", apps)
    adf = df[df["app"]==sel]
    aacts = [a for _, row in adf.iterrows() for a in row["suggested_actions"]]
    pp = round((adf["sentiment"]=="positive").mean()*100)
    np2 = 100 - pp
    p0a = sum(1 for a in aacts if a.get("priority")=="P0")
    p1a = sum(1 for a in aacts if a.get("priority")=="P1")

    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kcard("h-blue","v-blue","s-blue","Bundles Analyzed",str(len(adf)),f"for {sel}"), unsafe_allow_html=True)
    with c2: st.markdown(kcard("h-green","v-green","s-green","Positive Sentiment",f"{pp}%","Good signal" if pp>=50 else "Low"), unsafe_allow_html=True)
    with c3: st.markdown(kcard("h-red","v-red","s-red","Negative Sentiment",f"{np2}%","Needs attention"), unsafe_allow_html=True)
    with c4: st.markdown(kcard("h-orange","v-orange","s-orange","P0 Critical",str(p0a),"Fix immediately"), unsafe_allow_html=True)

    st.write("")
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="ccard-red"><div class="ccard-title">Top pain points</div>', unsafe_allow_html=True)
        pains = [p for _, row in adf.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"],list) else []) if isinstance(p,str) and len(p)>10]
        for p in pains[:5]: st.markdown(f'<div class="prow">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains: st.caption("No pain points detected")
        st.markdown('<br><div class="ccard-title">Top delighters</div>', unsafe_allow_html=True)
        dels = [d for _, row in adf.iterrows() for d in (row["delighters"] if isinstance(row["delighters"],list) else []) if isinstance(d,str) and len(d)>10]
        for d in dels[:5]: st.markdown(f'<div class="drow">{d[:160]}</div>', unsafe_allow_html=True)
        if not dels: st.caption("No delighters detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="ccard"><div class="ccard-title">Recommended actions</div>', unsafe_allow_html=True)
        if aacts:
            for a in aacts:
                oc2 = {"Engineering":"eng","Product":"prd","Design":"des"}.get(a.get("owner",""),"eng")
                pc2 = {"P0":"p0","P1":"p1","P2":"p2"}.get(a.get("priority",""),"p1")
                st.markdown(f'<div class="arow"><span class="badge {pc2}">{a.get("priority","")}</span> <span class="badge {oc2}">{a.get("owner","")}</span> {a.get("action","")}</div>', unsafe_allow_html=True)
        else: st.caption("No actions flagged")
        st.markdown('<br><div class="ccard-title">AI summaries</div>', unsafe_allow_html=True)
        for _, row in adf.head(5).iterrows():
            bc = "pos" if row["sentiment"]=="positive" else "neg"
            st.markdown(f'<div class="srow"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "Action Board":
    st.markdown('<div class="page-hdr">Action Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Action Board</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2 = st.columns(2)
    with f1: pf = st.multiselect("Priority", ["P0","P1","P2"], default=["P0","P1","P2"])
    with f2: of = st.multiselect("Owner", ["Engineering","Product","Design"], default=["Engineering","Product","Design"])

    filt = af.copy()
    if pf: filt = filt[filt["priority"].isin(pf)]
    if of: filt = filt[filt["owner"].isin(of)]

    st.write("")
    c1,c2,c3 = st.columns(3)
    p0f = int((filt["priority"]=="P0").sum()) if len(filt) else 0
    engf = int((filt["owner"]=="Engineering").sum()) if len(filt) else 0
    with c1: st.markdown(kcard("h-blue","v-blue","s-blue","Total Actions",str(len(filt)),"Filtered results"), unsafe_allow_html=True)
    with c2: st.markdown(kcard("h-red","v-red","s-red","P0 Critical",str(p0f),"Fix immediately"), unsafe_allow_html=True)
    with c3: st.markdown(kcard("h-dark","v-dark","","Engineering",str(engf),"Actions assigned"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="ccard"><div class="ccard-title">All recommended actions</div>', unsafe_allow_html=True)
    if len(filt):
        for _, row in filt.sort_values("priority").iterrows():
            oc2 = {"Engineering":"eng","Product":"prd","Design":"des"}.get(row["owner"],"eng")
            pc2 = {"P0":"p0","P1":"p1","P2":"p2"}.get(row["priority"],"p1")
            st.markdown(f'<div class="arow"><span class="badge {pc2}">{row["priority"]}</span> <span class="badge {oc2}">{row["owner"]}</span> {row["action"]}</div>', unsafe_allow_html=True)
    else: st.caption("No actions match filters")
    st.markdown('</div>', unsafe_allow_html=True)


elif page == "Full Results":
    st.markdown('<div class="page-hdr">Full Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Full Results</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2 = st.columns(2)
    with f1: sf = st.multiselect("Sentiment", ["positive","negative"], default=["positive","negative"])
    with f2: appf = st.multiselect("App", apps, default=[])

    rdf = df.copy()
    if sf: rdf = rdf[rdf["sentiment"].isin(sf)]
    if appf: rdf = rdf[rdf["app"].isin(appf)]

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(kcard("h-blue","v-blue","s-blue","Showing",str(len(rdf)),"bundles"), unsafe_allow_html=True)
    with c2: st.markdown(kcard("h-green","v-green","s-green","Positive",str((rdf["sentiment"]=="positive").sum()),"bundles"), unsafe_allow_html=True)
    with c3: st.markdown(kcard("h-red","v-red","s-red","Negative",str((rdf["sentiment"]=="negative").sum()),"bundles"), unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="ccard"><div class="ccard-title">Results table</div>', unsafe_allow_html=True)
    disp = rdf[["app","sentiment","summary"]].copy()
    disp.columns = ["App","Sentiment","AI Summary"]
    st.dataframe(disp, use_container_width=True, height=460, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    st.download_button("Download CSV", df.to_csv(index=False), "voc_results.csv", "text/csv")
