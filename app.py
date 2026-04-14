import streamlit as st
import pandas as pd
import ast
import os

st.set_page_config(page_title="VoC Intelligence Engine", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

section[data-testid="stSidebar"]{background:#111827!important;min-width:240px!important;max-width:240px!important;}
section[data-testid="stSidebar"]>div{padding:1.5rem 1.2rem;}
section[data-testid="stSidebar"] *{color:#9ca3af!important;}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] strong{color:#fff!important;}

.main .block-container{background:#f9fafb;padding:2rem 2.5rem;max-width:100%;}

.page-title{font-size:22px;font-weight:700;color:#111827;margin:0 0 2px;}
.breadcrumb{font-size:12px;color:#9ca3af;margin-bottom:1.5rem;}

.mcard{background:#fff;border-radius:10px;padding:1.25rem 1.4rem;border:1px solid #e5e7eb;height:120px;position:relative;}
.mcard-dark{background:#111827;border-radius:10px;padding:1.25rem 1.4rem;height:120px;position:relative;}
.mc-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6b7280;margin-bottom:8px;}
.mc-label-dk{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#4b5563;margin-bottom:8px;}
.mc-val{font-size:34px;font-weight:700;color:#111827;line-height:1;}
.mc-val-dk{font-size:34px;font-weight:700;color:#fff;line-height:1;}
.mc-sub-g{font-size:12px;color:#10b981;font-weight:500;margin-top:6px;}
.mc-sub-r{font-size:12px;color:#ef4444;font-weight:500;margin-top:6px;}
.mc-sub-gr{font-size:12px;color:#6b7280;font-weight:500;margin-top:6px;}

.mc-icon{position:absolute;top:1.25rem;right:1.4rem;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;}
.icon-g{background:#d1fae5;}
.icon-r{background:#fee2e2;}
.icon-b{background:#dbeafe;}
.icon-dk{background:#1f2937;}

.ccard{background:#fff;border-radius:10px;padding:1.25rem 1.4rem;border:1px solid #e5e7eb;margin-top:1rem;}
.ccard-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6b7280;margin-bottom:1rem;}

.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;margin:2px;}
.pos{background:#d1fae5;color:#065f46;}
.neg{background:#fee2e2;color:#991b1b;}
.p0{background:#fee2e2;color:#991b1b;}
.p1{background:#fef3c7;color:#92400e;}
.p2{background:#d1fae5;color:#065f46;}
.eng{background:#dbeafe;color:#1e40af;}
.prd{background:#ede9fe;color:#5b21b6;}
.des{background:#fce7f3;color:#9d174d;}

.action-row{background:#f9fafb;border:1px solid #f3f4f6;border-radius:8px;padding:9px 12px;margin:4px 0;font-size:13px;color:#374151;}
.pain-row{border-left:3px solid #ef4444;background:#fff5f5;border-radius:0 6px 6px 0;padding:8px 12px;margin:4px 0;font-size:13px;color:#374151;}
.delight-row{border-left:3px solid #10b981;background:#f0fdf4;border-radius:0 6px 6px 0;padding:8px 12px;margin:4px 0;font-size:13px;color:#374151;}
.summary-row{background:#f9fafb;border:1px solid #f3f4f6;border-radius:8px;padding:9px 12px;margin:4px 0;font-size:13px;color:#374151;}

.sstat{background:#1f2937;border-radius:8px;padding:10px 12px;margin-bottom:8px;}
.sstat-lbl{font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#4b5563!important;}
.sstat-val{font-size:18px;font-weight:700;color:#fff!important;margin-top:2px;}
.ssec{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#374151!important;margin:1.2rem 0 .5rem;}
</style>
""", unsafe_allow_html=True)


def icon_svg(shape, color):
    if shape == "bar":
        return f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round"><rect x="3" y="12" width="4" height="9"/><rect x="10" y="6" width="4" height="15"/><rect x="17" y="3" width="4" height="18"/></svg>'
    elif shape == "up":
        return f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>'
    elif shape == "down":
        return f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>'
    elif shape == "alert":
        return f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
    elif shape == "users":
        return f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>'
    return ""


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

# SIDEBAR
with st.sidebar:
    st.markdown('<strong style="font-size:18px;color:#fff!important">VoC Intelligence</strong>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:#1f2937;margin:12px 0">', unsafe_allow_html=True)

    page = st.radio("", ["Dashboard","App Explorer","Action Board","Full Results"], label_visibility="collapsed")

    st.markdown('<div class="ssec">Overview</div>', unsafe_allow_html=True)
    for lbl, val in [("Reviews analyzed","200,000"),("Apps covered","20"),("Actions flagged",str(ta)),("Bundles processed",str(total))]:
        st.markdown(f'<div class="sstat"><div class="sstat-lbl">{lbl}</div><div class="sstat-val">{val}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="ssec">Model</div>', unsafe_allow_html=True)
    for lbl, val in [("Architecture","FLAN-T5 + LoRA"),("Checkpoint","3,449 steps"),("GPU","Tesla T4"),("Accuracy","85.74%")]:
        st.markdown(f'<div class="sstat"><div class="sstat-lbl">{lbl}</div><div style="font-size:13px;color:#9ca3af;margin-top:2px">{val}</div></div>', unsafe_allow_html=True)

    st.markdown('<br><p style="font-size:11px;color:#374151;text-align:center">Tanushree Poojary · UIUC 2026</p>', unsafe_allow_html=True)


if page == "Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Dashboard</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f'''<div class="mcard">
            <div class="mc-label">Total bundles</div>
            <div class="mc-val">{total}</div>
            <div class="mc-sub-g">100 samples processed</div>
            <div class="mc-icon icon-b">{icon_svg("bar","#2563eb")}</div>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="mcard">
            <div class="mc-label">Positive sentiment</div>
            <div class="mc-val">{pos}</div>
            <div class="mc-sub-g">50% of all bundles</div>
            <div class="mc-icon icon-g">{icon_svg("up","#059669")}</div>
        </div>''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''<div class="mcard">
            <div class="mc-label">Negative sentiment</div>
            <div class="mc-val">{neg}</div>
            <div class="mc-sub-r">50% needs attention</div>
            <div class="mc-icon icon-r">{icon_svg("down","#dc2626")}</div>
        </div>''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''<div class="mcard-dark">
            <div class="mc-label-dk">Critical P0 issues</div>
            <div class="mc-val-dk">{p0c}</div>
            <div class="mc-sub-r">Fix immediately</div>
            <div class="mc-icon icon-dk">{icon_svg("alert","#ef4444")}</div>
        </div>''', unsafe_allow_html=True)

    st.write("")
    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment by app</div>', unsafe_allow_html=True)
        app_sent = df.groupby(["app","sentiment"]).size().unstack(fill_value=0)
        st.bar_chart(app_sent, height=260, color=["#ef4444","#10b981"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment trend across bundles</div>', unsafe_allow_html=True)
        trend = df.sort_values("sample_id").copy()
        trend["positive"] = (trend["sentiment"]=="positive").cumsum()
        trend["negative"] = (trend["sentiment"]=="negative").cumsum()
        st.line_chart(trend.set_index("sample_id")[["positive","negative"]], height=180, color=["#10b981","#ef4444"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ccard"><div class="ccard-title">Sentiment split</div>', unsafe_allow_html=True)
        sc = df["sentiment"].value_counts().reset_index()
        sc.columns = ["sentiment","count"]
        st.bar_chart(sc.set_index("sentiment"), height=150, color=["#6366f1"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard"><div class="ccard-title">Action owners</div>', unsafe_allow_html=True)
        oc = af["owner"].value_counts().reset_index()
        oc.columns = ["owner","count"]
        st.bar_chart(oc.set_index("owner"), height=150, color=["#111827"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ccard"><div class="ccard-title">Priority distribution</div>', unsafe_allow_html=True)
        pc = af["priority"].value_counts().reset_index()
        pc.columns = ["priority","count"]
        st.bar_chart(pc.set_index("priority"), height=150, color=["#f59e0b"])
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
    with c1:
        st.markdown(f'<div class="mcard"><div class="mc-label">Bundles</div><div class="mc-val">{len(adf)}</div><div class="mc-icon icon-b">{icon_svg("bar","#2563eb")}</div></div>', unsafe_allow_html=True)
    with c2:
        sub_c = "mc-sub-g" if pp>=50 else "mc-sub-r"
        ic = "icon-g" if pp>=50 else "icon-r"
        sv = icon_svg("up","#059669") if pp>=50 else icon_svg("down","#dc2626")
        st.markdown(f'<div class="mcard"><div class="mc-label">Positive sentiment</div><div class="mc-val">{pp}%</div><div class="{sub_c}">{"Good signal" if pp>=50 else "Needs attention"}</div><div class="mc-icon {ic}">{sv}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="mcard"><div class="mc-label">P0 critical</div><div class="mc-val">{p0a}</div><div class="mc-sub-r">Fix immediately</div><div class="mc-icon icon-r">{icon_svg("alert","#dc2626")}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="mcard-dark"><div class="mc-label-dk">P1 this sprint</div><div class="mc-val-dk">{p1a}</div><div class="mc-icon icon-dk">{icon_svg("users","#9ca3af")}</div></div>', unsafe_allow_html=True)

    st.write("")
    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="ccard"><div class="ccard-title">Top pain points</div>', unsafe_allow_html=True)
        pains = [p for _, row in adf.iterrows() for p in (row["pain_points"] if isinstance(row["pain_points"],list) else []) if isinstance(p,str) and len(p)>10]
        for p in pains[:5]: st.markdown(f'<div class="pain-row">{p[:160]}</div>', unsafe_allow_html=True)
        if not pains: st.caption("No pain points detected")
        st.markdown('<br><div class="ccard-title">Top delighters</div>', unsafe_allow_html=True)
        dels = [d for _, row in adf.iterrows() for d in (row["delighters"] if isinstance(row["delighters"],list) else []) if isinstance(d,str) and len(d)>10]
        for d in dels[:5]: st.markdown(f'<div class="delight-row">{d[:160]}</div>', unsafe_allow_html=True)
        if not dels: st.caption("No delighters detected")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="ccard"><div class="ccard-title">Recommended actions</div>', unsafe_allow_html=True)
        if aacts:
            for a in aacts:
                oc2 = {"Engineering":"eng","Product":"prd","Design":"des"}.get(a.get("owner",""),"eng")
                pc2 = {"P0":"p0","P1":"p1","P2":"p2"}.get(a.get("priority",""),"p1")
                st.markdown(f'<div class="action-row"><span class="badge {pc2}">{a.get("priority","")}</span> <span class="badge {oc2}">{a.get("owner","")}</span> {a.get("action","")}</div>', unsafe_allow_html=True)
        else: st.caption("No actions flagged")
        st.markdown('<br><div class="ccard-title">AI summaries</div>', unsafe_allow_html=True)
        for _, row in adf.head(5).iterrows():
            bc = "pos" if row["sentiment"]=="positive" else "neg"
            st.markdown(f'<div class="summary-row"><span class="badge {bc}">{row["sentiment"]}</span> &nbsp;{row["summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "Action Board":
    st.markdown('<div class="page-title">Action Board</div>', unsafe_allow_html=True)
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
    with c1: st.markdown(f'<div class="mcard"><div class="mc-label">Total actions</div><div class="mc-val">{len(filt)}</div><div class="mc-icon icon-b">{icon_svg("bar","#2563eb")}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="mcard"><div class="mc-label">P0 critical</div><div class="mc-val">{p0f}</div><div class="mc-sub-r">Fix immediately</div><div class="mc-icon icon-r">{icon_svg("alert","#dc2626")}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="mcard-dark"><div class="mc-label-dk">Engineering actions</div><div class="mc-val-dk">{engf}</div><div class="mc-icon icon-dk">{icon_svg("users","#9ca3af")}</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="ccard"><div class="ccard-title">All recommended actions</div>', unsafe_allow_html=True)
    if len(filt):
        for _, row in filt.sort_values("priority").iterrows():
            oc2 = {"Engineering":"eng","Product":"prd","Design":"des"}.get(row["owner"],"eng")
            pc2 = {"P0":"p0","P1":"p1","P2":"p2"}.get(row["priority"],"p1")
            st.markdown(f'<div class="action-row"><span class="badge {pc2}">{row["priority"]}</span> <span class="badge {oc2}">{row["owner"]}</span> {row["action"]}</div>', unsafe_allow_html=True)
    else: st.caption("No actions match filters")
    st.markdown('</div>', unsafe_allow_html=True)


elif page == "Full Results":
    st.markdown('<div class="page-title">Full Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="breadcrumb">Home &rsaquo; Full Results</div>', unsafe_allow_html=True)

    st.write("")
    f1,f2 = st.columns(2)
    with f1: sf = st.multiselect("Sentiment", ["positive","negative"], default=["positive","negative"])
    with f2: appf = st.multiselect("App", apps, default=[])

    rdf = df.copy()
    if sf: rdf = rdf[rdf["sentiment"].isin(sf)]
    if appf: rdf = rdf[rdf["app"].isin(appf)]

    st.caption(f"Showing {len(rdf)} of {total} bundles")
    st.markdown('<div class="ccard">', unsafe_allow_html=True)
    disp = rdf[["app","sentiment","summary"]].copy()
    disp.columns = ["App","Sentiment","AI Summary"]
    st.dataframe(disp, use_container_width=True, height=460, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    st.download_button("Download results CSV", df.to_csv(index=False), "voc_results.csv", "text/csv")
