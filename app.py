
import streamlit as st
import pandas as pd
import plotly.express as px

from data import get_camps, get_warehouses
from scoring import add_priority_scores
from allocation import allocate_supplies
from routing import find_route


st.set_page_config(
    page_title="ReliefRoute | Operations Center",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background:#f4f6f8; }
.block-container { padding-top:1.4rem; padding-bottom:3rem; max-width:1500px; }

.demo-banner {
    background:#fff4d6; border:1px solid #e7c76b; color:#594700;
    padding:9px 16px; border-radius:4px; font-size:13px;
    font-weight:600; margin-bottom:18px;
}
.demo-banner span { font-family:'IBM Plex Mono'; margin-right:12px; }

.main-header {
    display:flex; justify-content:space-between; align-items:flex-end;
    border-bottom:1px solid #d8dde3; padding-bottom:15px; margin-bottom:20px;
}
.system-name { font-size:25px; font-weight:700; color:#17212b; }
.system-subtitle { font-size:12px; color:#687581; margin-top:4px; }
.system-status {
    font-family:'IBM Plex Mono'; font-size:11px; color:#23613f;
    background:#e9f5ee; border:1px solid #b9dcc7; padding:6px 10px; border-radius:3px;
}

.section-title { font-size:16px; font-weight:700; color:#17212b; margin:24px 0 10px; }
.section-description { color:#687581; font-size:12px; margin:-5px 0 15px; }

.metric {
    background:white; border:1px solid #d8dde3; border-radius:5px;
    padding:15px 17px; min-height:95px;
}
.metric-label {
    color:#687581; font-size:11px; text-transform:uppercase;
    letter-spacing:.6px; font-weight:600;
}
.metric-value { color:#17212b; font-size:27px; font-weight:700; margin-top:6px; }
.metric-detail { color:#7b8791; font-size:11px; margin-top:3px; }

.alert-critical {
    background:#fff0ef; border-left:4px solid #b42318;
    border-top:1px solid #ead0cd; border-right:1px solid #ead0cd;
    border-bottom:1px solid #ead0cd; padding:12px 15px; margin-bottom:8px;
}
.alert-warning {
    background:#fff8e7; border-left:4px solid #b7791f;
    border-top:1px solid #ead9b5; border-right:1px solid #ead9b5;
    border-bottom:1px solid #ead9b5; padding:12px 15px; margin-bottom:8px;
}
.alert-title { font-size:12px; font-weight:700; color:#17212b; }
.alert-text { font-size:12px; color:#53616c; margin-top:3px; }

.panel {
    background:white; border:1px solid #d8dde3; border-radius:5px;
    padding:18px; margin-bottom:15px;
}
.panel-title { font-size:13px; font-weight:700; color:#17212b; margin-bottom:12px; }

section[data-testid="stSidebar"] { background:#17212b; }
section[data-testid="stSidebar"] * { color:#e9eef2; }
.sidebar-logo { font-size:20px; font-weight:700; color:white; }
.sidebar-subtitle { color:#9eabb5; font-size:11px; margin-bottom:25px; }
.sidebar-divider { border-top:1px solid #34424d; margin:18px 0; }
.sidebar-status {
    font-family:'IBM Plex Mono'; font-size:10px; color:#aebbc4; line-height:1.8;
}

.stButton > button {
    border-radius:4px; border:1px solid #b8c1c8;
    background:white; color:#17212b; font-weight:600; font-size:12px;
}
button[kind="primary"] {
    background:#244d69 !important; border-color:#244d69 !important; color:white !important;
}
.footer {
    border-top:1px solid #d8dde3; margin-top:40px; padding-top:12px;
    color:#7b8791; font-size:10px; display:flex; justify-content:space-between;
}
.mono { font-family:'IBM Plex Mono'; }
</style>
""", unsafe_allow_html=True)


# Load backend data using the functions that actually exist in data.py.
raw_camps = get_camps()
raw_warehouses = get_warehouses()

# Add the Priority Score and Priority Level columns required by allocation.py.
camps = add_priority_scores(raw_camps)
warehouses = raw_warehouses.copy()

if "approved" not in st.session_state:
    st.session_state.approved = False
if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False


with st.sidebar:
    st.markdown('<div class="sidebar-logo">RELIEFROUTE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Humanitarian Logistics Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    page = st.radio(
        "OPERATIONS",
        [
            "Operations Overview",
            "Field Reports",
            "Priority Assessment",
            "Supply Allocation",
            "Route Planning",
            "Performance",
            "Decision Approval"
        ]
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-status">
    SYSTEM STATUS<br>
    ● DATA ENGINE &nbsp;&nbsp; READY<br>
    ● PRIORITY ENGINE &nbsp; READY<br>
    ● ROUTE ENGINE &nbsp;&nbsp;&nbsp; READY<br>
    ● APPROVAL GATE &nbsp;&nbsp; ACTIVE
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="demo-banner">
<span>DEMO • SIMULATION DATA</span>
This prototype is for demonstration only and is not connected to a live disaster-response operation.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<div>
<div class="system-name">ReliefRoute Operations Center</div>
<div class="system-subtitle">
Flood response coordination • Assam scenario • Initial 72-hour response window
</div>
</div>
<div class="system-status">● SYSTEM OPERATIONAL</div>
</div>
""", unsafe_allow_html=True)


if page == "Operations Overview":

    st.markdown('<div class="section-title">Situation Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Current simulated operational picture.</div>', unsafe_allow_html=True)

    critical = int((camps["Priority Level"] == "CRITICAL").sum())
    high = int((camps["Priority Level"] == "HIGH").sum())
    total_people = int(camps["People"].sum())

    c1, c2, c3, c4 = st.columns(4)

    for col, label, value, detail in [
        (c1, "Affected Camps", len(camps), f"{total_people:,} people represented"),
        (c2, "Critical Camps", critical, "Immediate attention required"),
        (c3, "High Priority", high, "Elevated operational need"),
        (c4, "Supply Points", len(warehouses), "Simulated warehouses")
    ]:
        with col:
            st.markdown(f"""
            <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-detail">{detail}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Operational Alerts</div>', unsafe_allow_html=True)

    critical_rows = camps[camps["Priority Level"] == "CRITICAL"]

    if len(critical_rows):
        for _, row in critical_rows.iterrows():
            st.markdown(f"""
            <div class="alert-critical">
            <div class="alert-title">PRIORITY ALERT — {row["Camp"]}</div>
            <div class="alert-text">
            Priority score {row["Priority Score"]}/100. Camp requires immediate coordinator review.
            </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-warning">
        <div class="alert-title">NO CRITICAL CAMPS IDENTIFIED</div>
        <div class="alert-text">Continue monitoring incoming field reports.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Camp Priority Register</div>', unsafe_allow_html=True)

    register = camps[[
        "Camp", "People", "Priority Score", "Priority Level",
        "Health Risk", "Vulnerable", "Time Without Aid", "Isolation"
    ]].sort_values("Priority Score", ascending=False)

    st.dataframe(
        register,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Priority Score": st.column_config.ProgressColumn(
                "Priority Score", min_value=0, max_value=100, format="%.1f"
            )
        }
    )


elif page == "Field Reports":

    st.markdown('<div class="section-title">Incoming Field Reports</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
    Simulated reports representing the type of unstructured information received by relief coordinators.
    </div>
    """, unsafe_allow_html=True)

    reports = [
        ("Camp 4", "08:14", "Field volunteer",
         "Around 610 people here. Water is running low. Several elderly people and children are sick. Road from the south is flooded."),
        ("Camp 2", "08:37", "Local coordinator",
         "About 520 people. Medical supplies urgently needed. Water access is limited and the main road cannot be used."),
        ("Camp 5", "09:05", "Volunteer network",
         "430 people currently sheltering here. Food available for a short period but water supplies are decreasing.")
    ]

    for camp_name, time, source, message in reports:
        st.markdown(f"""
        <div class="panel">
        <div class="panel-title">{camp_name}
        <span style="float:right;font-family:'IBM Plex Mono';font-size:10px;color:#71808b">
        {time} • {source}</span></div>
        <div style="background:#f7f8fa;border:1px solid #e1e5e8;padding:12px;
        border-radius:3px;font-size:12px;color:#45515b;line-height:1.6">
        {message}
        </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Process report — {camp_name}", key=f"process_{camp_name}"):
            row = camps[camps["Camp"] == camp_name].iloc[0]
            st.success("Report converted into a structured operational record.")
            a, b, c, d = st.columns(4)
            a.metric("Population", int(row["People"]))
            b.metric("Health Risk", int(row["Health Risk"]))
            c.metric("Vulnerable", int(row["Vulnerable"]))
            d.metric("Priority", f'{row["Priority Score"]:.1f}')
            st.info(
                f'Priority classification: {row["Priority Level"]}. '
                'The extracted information supports coordinator assessment; it does not authorize deployment.'
            )


elif page == "Priority Assessment":

    st.markdown('<div class="section-title">Priority Assessment</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
    Transparent scoring model used to identify which camps require attention first.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
    <div class="panel-title">Priority Model</div>
    <div style="font-family:'IBM Plex Mono';font-size:13px;color:#33424e;line-height:2">
    PRIORITY SCORE =
    <b>0.35 × Health Risk</b> +
    <b>0.25 × Vulnerable</b> +
    <b>0.25 × Time Without Aid</b> +
    <b>0.15 × Isolation</b>
    </div>
    <div style="margin-top:10px;font-size:11px;color:#71808b">
    Scores are illustrative for this prototype. Weighting should be validated with humanitarian-response experts before operational use.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        camps[[
            "Camp", "Health Risk", "Vulnerable", "Time Without Aid",
            "Isolation", "Priority Score", "Priority Level"
        ]].sort_values("Priority Score", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        camps.sort_values("Priority Score"),
        x="Priority Score",
        y="Camp",
        orientation="h",
        text="Priority Score"
    )
    fig.update_layout(
        height=400, margin=dict(l=10, r=10, t=20, b=20),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter", size=12, color="#34424e"),
        xaxis=dict(range=[0, 100], gridcolor="#e5e9ed"),
        yaxis=dict(gridcolor="white")
    )
    st.plotly_chart(fig, use_container_width=True)


elif page == "Supply Allocation":

    st.markdown('<div class="section-title">Supply Allocation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
    Proposed allocation of limited warehouse resources against camp requirements.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-warning">
    <div class="alert-title">DECISION SUPPORT ONLY</div>
    <div class="alert-text">
    Allocation recommendations require coordinator review before deployment.
    </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generate Relief Allocation", type="primary"):
        st.session_state.plan_generated = True

    if st.session_state.plan_generated:
        allocations, remaining = allocate_supplies(camps, warehouses)

        st.markdown('<div class="section-title">Recommended Allocation Plan</div>', unsafe_allow_html=True)

        if allocations:
            st.dataframe(
                pd.DataFrame(allocations),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No allocation was generated.")

        st.markdown('<div class="section-title">Remaining Warehouse Inventory</div>', unsafe_allow_html=True)
        st.dataframe(
            remaining,
            use_container_width=True,
            hide_index=True
        )


elif page == "Route Planning":

    st.markdown('<div class="section-title">Route Planning</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
    Flood-aware routing excludes roads marked as inaccessible in the simulation.
    </div>
    """, unsafe_allow_html=True)

    selected_camp = st.selectbox("Destination camp", camps["Camp"].tolist())
    selected_warehouse = st.selectbox("Dispatch warehouse", warehouses["Warehouse"].tolist())

    if st.button("Calculate Safe Route", type="primary"):
        route, distance = find_route(selected_warehouse, selected_camp)

        if route:
            st.markdown("""
            <div class="alert-warning">
            <div class="alert-title">ROUTE RECOMMENDATION</div>
            <div class="alert-text">
            Route generated using the simulated road network. Confirm physical road conditions before deployment.
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="panel">
            <div class="panel-title">Recommended Route</div>
            <div style="font-family:'IBM Plex Mono';font-size:13px;color:#34424e;line-height:2">
            {" → ".join(route)}
            </div>
            <div style="margin-top:12px;font-size:11px;color:#71808b">
            Estimated route distance: <b>{distance} km</b>
            </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-critical">
            <div class="alert-title">NO SAFE ROUTE FOUND</div>
            <div class="alert-text">
            The simulated road network does not contain an available route.
            </div>
            </div>
            """, unsafe_allow_html=True)


elif page == "Performance":

    st.markdown('<div class="section-title">Evaluation Framework</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
    Example evaluation view. Values below are illustrative placeholders and are not experimental results.
    </div>
    """, unsafe_allow_html=True)

    comparison = pd.DataFrame({
        "Strategy": ["First-Come-First-Served", "Nearest Warehouse", "ReliefRoute"],
        "Critical Demand Fulfilled (%)": [62, 71, 91],
        "Camps Below Minimum": [7, 5, 2],
        "Average Response Time (h)": [8.2, 6.4, 4.1]
    })

    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Evaluation Metrics</div>', unsafe_allow_html=True)

    for metric in [
        "Critical demand fulfilled",
        "Time to first delivery",
        "Camps below minimum supply",
        "Vulnerable-population coverage",
        "Total route distance",
        "Unmet demand",
        "Flooded-road violations"
    ]:
        st.markdown(
            f'<div style="background:white;border:1px solid #d8dde3;padding:9px 12px;margin-bottom:5px;font-size:12px;color:#45515b">{metric}</div>',
            unsafe_allow_html=True
        )


elif page == "Decision Approval":

    st.markdown('<div class="section-title">Decision Approval</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-description">
    Human coordinator remains responsible for approving operational recommendations.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
    <div class="panel-title">Relief Deployment Recommendation</div>
    <div style="font-size:12px;color:#52616d;line-height:2">
    <b>Priority:</b> Critical camps first<br>
    <b>Allocation:</b> Warehouse stock constrained<br>
    <b>Routing:</b> Flooded roads excluded<br>
    <b>Approval:</b> Human coordinator required
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-warning">
    <div class="alert-title">REVIEW REQUIRED</div>
    <div class="alert-text">
    Verify field reports, road conditions, inventory and safety conditions before approving deployment.
    </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Approve Recommendation", type="primary", use_container_width=True):
            st.session_state.approved = True

    with c2:
        if st.button("Request Reassessment", use_container_width=True):
            st.session_state.approved = False
            st.warning("Recommendation returned for coordinator reassessment.")

    if st.session_state.approved:
        st.success("Recommendation marked APPROVED in the demonstration workflow.")
        st.markdown(
            '<div class="mono" style="font-size:11px;color:#52705d">STATUS: APPROVED — DEMONSTRATION ONLY</div>',
            unsafe_allow_html=True
        )


st.markdown("""
<div class="footer">
<div>RELIEFROUTE AI • HUMANITARIAN LOGISTICS PROTOTYPE</div>
<div class="mono">DEMO BUILD • NOT FOR LIVE DEPLOYMENT</div>
</div>
""", unsafe_allow_html=True)
