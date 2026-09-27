import streamlit as st
import pandas as pd
import plotly.express as px

from data import camps, warehouses
from scoring import calculate_priority
from allocation import allocate_supplies
from routing import find_route


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReliefRoute | Operations Center",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f6f8;
}

/* Remove Streamlit top padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* ---------------------------------------------------------
   DEMO BANNER
--------------------------------------------------------- */

.demo-banner {
    background: #fff4d6;
    border: 1px solid #e7c76b;
    color: #594700;
    padding: 9px 16px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.2px;
    margin-bottom: 18px;
}

.demo-banner span {
    font-family: 'IBM Plex Mono', monospace;
    margin-right: 12px;
}

/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.main-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1px solid #d8dde3;
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.system-name {
    font-size: 25px;
    font-weight: 700;
    color: #17212b;
    letter-spacing: -0.5px;
}

.system-subtitle {
    font-size: 12px;
    color: #687581;
    margin-top: 4px;
}

.system-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #23613f;
    background: #e9f5ee;
    border: 1px solid #b9dcc7;
    padding: 6px 10px;
    border-radius: 3px;
}

/* ---------------------------------------------------------
   SECTION HEADERS
--------------------------------------------------------- */

.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #17212b;
    margin-top: 24px;
    margin-bottom: 10px;
}

.section-description {
    color: #687581;
    font-size: 12px;
    margin-top: -5px;
    margin-bottom: 15px;
}

/* ---------------------------------------------------------
   METRIC CARDS
--------------------------------------------------------- */

.metric {
    background: white;
    border: 1px solid #d8dde3;
    border-radius: 5px;
    padding: 15px 17px;
    min-height: 95px;
}

.metric-label {
    color: #687581;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 600;
}

.metric-value {
    color: #17212b;
    font-size: 27px;
    font-weight: 700;
    margin-top: 6px;
}

.metric-detail {
    color: #7b8791;
    font-size: 11px;
    margin-top: 3px;
}

/* ---------------------------------------------------------
   ALERTS
--------------------------------------------------------- */

.alert-critical {
    background: #fff0ef;
    border-left: 4px solid #b42318;
    border-top: 1px solid #ead0cd;
    border-right: 1px solid #ead0cd;
    border-bottom: 1px solid #ead0cd;
    padding: 12px 15px;
    margin-bottom: 8px;
}

.alert-warning {
    background: #fff8e7;
    border-left: 4px solid #b7791f;
    border-top: 1px solid #ead9b5;
    border-right: 1px solid #ead9b5;
    border-bottom: 1px solid #ead9b5;
    padding: 12px 15px;
    margin-bottom: 8px;
}

.alert-title {
    font-size: 12px;
    font-weight: 700;
    color: #17212b;
}

.alert-text {
    font-size: 12px;
    color: #53616c;
    margin-top: 3px;
}

/* ---------------------------------------------------------
   STATUS BADGES
--------------------------------------------------------- */

.badge {
    display: inline-block;
    padding: 3px 7px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
}

.badge-critical {
    color: #9e1b15;
    background: #fde8e7;
}

.badge-high {
    color: #875a00;
    background: #fff0c9;
}

.badge-medium {
    color: #315c86;
    background: #e8f1fa;
}

.badge-low {
    color: #3c654e;
    background: #e8f3ec;
}

/* ---------------------------------------------------------
   TABLES / PANELS
--------------------------------------------------------- */

.panel {
    background: white;
    border: 1px solid #d8dde3;
    border-radius: 5px;
    padding: 18px;
    margin-bottom: 15px;
}

.panel-title {
    font-size: 13px;
    font-weight: 700;
    color: #17212b;
    margin-bottom: 12px;
}

.panel-subtitle {
    font-size: 11px;
    color: #71808b;
    margin-bottom: 12px;
}

/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: #17212b;
}

section[data-testid="stSidebar"] * {
    color: #e9eef2;
}

section[data-testid="stSidebar"] .stRadio label {
    font-size: 13px;
}

.sidebar-logo {
    font-size: 20px;
    font-weight: 700;
    color: white;
    margin-bottom: 2px;
}

.sidebar-subtitle {
    color: #9eabb5;
    font-size: 11px;
    margin-bottom: 25px;
}

.sidebar-divider {
    border-top: 1px solid #34424d;
    margin: 18px 0;
}

.sidebar-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #aebbc4;
    line-height: 1.8;
}

/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

.stButton > button {
    border-radius: 4px;
    border: 1px solid #b8c1c8;
    background: white;
    color: #17212b;
    font-weight: 600;
    font-size: 12px;
}

.stButton > button:hover {
    border-color: #3c617d;
    color: #254b67;
}

/* Primary */
button[kind="primary"] {
    background: #244d69 !important;
    border-color: #244d69 !important;
    color: white !important;
}

/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */

.stSelectbox > div,
.stTextInput > div {
    font-size: 12px;
}

/* ---------------------------------------------------------
   FOOTER
--------------------------------------------------------- */

.footer {
    border-top: 1px solid #d8dde3;
    margin-top: 40px;
    padding-top: 12px;
    color: #7b8791;
    font-size: 10px;
    display: flex;
    justify-content: space-between;
}

.mono {
    font-family: 'IBM Plex Mono', monospace;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "approved" not in st.session_state:
    st.session_state.approved = False

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def priority_badge(level):

    level = str(level).upper()

    if level == "CRITICAL":
        return '<span class="badge badge-critical">CRITICAL</span>'

    if level == "HIGH":
        return '<span class="badge badge-high">HIGH</span>'

    if level == "MEDIUM":
        return '<span class="badge badge-medium">MEDIUM</span>'

    return '<span class="badge badge-low">LOW</span>'


def get_priority(camp):

    return calculate_priority(
        camp["health_risk"],
        camp["vulnerable"],
        camp["time_without_aid"],
        camp["isolation"]
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">RELIEFROUTE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Humanitarian Logistics Operations</div>',
        unsafe_allow_html=True
    )

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
        ],
        label_visibility="visible"
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-status">
        SYSTEM STATUS<br>
        ● DATA ENGINE &nbsp;&nbsp; READY<br>
        ● PRIORITY ENGINE &nbsp; READY<br>
        ● ROUTE ENGINE &nbsp;&nbsp;&nbsp; READY<br>
        ● APPROVAL GATE &nbsp;&nbsp; ACTIVE
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GLOBAL HEADER
# ============================================================

st.markdown(
    """
    <div class="demo-banner">
        <span>DEMO • SIMULATION DATA</span>
        This prototype is for demonstration only and is not connected to a live disaster-response operation.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-header">
        <div>
            <div class="system-name">ReliefRoute Operations Center</div>
            <div class="system-subtitle">
                Flood response coordination • Assam scenario • Initial 72-hour response window
            </div>
        </div>
        <div class="system-status">
            ● SYSTEM OPERATIONAL
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OPERATIONS OVERVIEW
# ============================================================

if page == "Operations Overview":

    st.markdown(
        '<div class="section-title">Situation Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Current simulated operational picture.</div>',
        unsafe_allow_html=True
    )

    priorities = []

    for camp in camps:
        score, level = get_priority(camp)
        priorities.append({
            "Camp": camp["name"],
            "Priority": round(score, 1),
            "Level": level
        })

    priority_df = pd.DataFrame(priorities)

    critical = len(priority_df[priority_df["Level"] == "CRITICAL"])
    high = len(priority_df[priority_df["Level"] == "HIGH"])
    total_people = sum(c["population"] for c in camps)
    warehouses_count = len(warehouses)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Affected Camps</div>
                <div class="metric-value">{len(camps)}</div>
                <div class="metric-detail">{total_people:,} people represented</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Critical Camps</div>
                <div class="metric-value">{critical}</div>
                <div class="metric-detail">Immediate attention required</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">High Priority</div>
                <div class="metric-value">{high}</div>
                <div class="metric-detail">Elevated operational need</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Supply Points</div>
                <div class="metric-value">{warehouses_count}</div>
                <div class="metric-detail">Simulated warehouses</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Operational Alerts</div>',
        unsafe_allow_html=True
    )

    critical_camps = priority_df[
        priority_df["Level"] == "CRITICAL"
    ]

    if len(critical_camps) > 0:

        for _, row in critical_camps.iterrows():

            st.markdown(
                f"""
                <div class="alert-critical">
                    <div class="alert-title">
                        PRIORITY ALERT — {row["Camp"]}
                    </div>
                    <div class="alert-text">
                        Priority score {row["Priority"]}/100.
                        Camp requires immediate review by the coordinator.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div class="alert-warning">
                <div class="alert-title">NO CRITICAL CAMPS IDENTIFIED</div>
                <div class="alert-text">
                    Continue monitoring incoming field reports.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Camp Priority Register</div>',
        unsafe_allow_html=True
    )

    display_df = priority_df.sort_values(
        "Priority",
        ascending=False
    ).reset_index(drop=True)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Priority": st.column_config.ProgressColumn(
                "Priority Score",
                min_value=0,
                max_value=100,
                format="%.1f"
            )
        }
    )


# ============================================================
# FIELD REPORTS
# ============================================================

elif page == "Field Reports":

    st.markdown(
        '<div class="section-title">Incoming Field Reports</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Simulated reports representing the type of unstructured information received by relief coordinators.
        </div>
        """,
        unsafe_allow_html=True
    )

    reports = [
        {
            "camp": "Camp 4",
            "time": "08:14",
            "source": "Field volunteer",
            "message": "Around 610 people here. Water is running low. Several elderly people and children are sick. Road from the south is flooded."
        },
        {
            "camp": "Camp 2",
            "time": "08:37",
            "source": "Local coordinator",
            "message": "About 520 people. Medical supplies urgently needed. Water access is limited and the main road cannot be used."
        },
        {
            "camp": "Camp 5",
            "time": "09:05",
            "source": "Volunteer network",
            "message": "430 people currently sheltering here. Food available for a short period but water supplies are decreasing."
        }
    ]

    for report in reports:

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">
                    {report["camp"]}
                    <span style="float:right;font-family:'IBM Plex Mono';font-size:10px;color:#71808b">
                    {report["time"]} • {report["source"]}
                    </span>
                </div>

                <div style="
                    background:#f7f8fa;
                    border:1px solid #e1e5e8;
                    padding:12px;
                    border-radius:3px;
                    font-size:12px;
                    color:#45515b;
                    line-height:1.6;
                ">
                    {report["message"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"Process report — {report['camp']}",
            key=f"process_{report['camp']}"
        ):

            matching = next(
                c for c in camps
                if c["name"] == report["camp"]
            )

            score, level = get_priority(matching)

            st.success("Report successfully converted into a structured operational record.")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Population", matching["population"])

            with col2:
                st.metric("Health Risk", matching["health_risk"])

            with col3:
                st.metric("Vulnerable", matching["vulnerable"])

            with col4:
                st.metric("Priority", f"{score:.1f}")

            st.markdown(
                f"""
                **Priority classification:** {level}

                **Decision note:** The extracted information is used to support
                the coordinator's assessment. The system does not automatically
                authorize deployment.
                """
            )


# ============================================================
# PRIORITY ASSESSMENT
# ============================================================

elif page == "Priority Assessment":

    st.markdown(
        '<div class="section-title">Priority Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Transparent scoring model used to identify which camps require attention first.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="panel">

        <div class="panel-title">Priority Model</div>

        <div style="font-family:'IBM Plex Mono';font-size:13px;color:#33424e;line-height:2">

        PRIORITY SCORE =

        <b>0.35 × Health Risk</b>
        +
        <b>0.25 × Vulnerable Population</b>
        +
        <b>0.25 × Time Without Aid</b>
        +
        <b>0.15 × Isolation</b>

        </div>

        <div style="margin-top:10px;font-size:11px;color:#71808b">
        Scores are illustrative for this prototype. Weighting should be validated with humanitarian-response experts before operational use.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    rows = []

    for camp in camps:

        score, level = get_priority(camp)

        rows.append({
            "Camp": camp["name"],
            "Health Risk": camp["health_risk"],
            "Vulnerable": camp["vulnerable"],
            "Hours Without Aid": camp["time_without_aid"],
            "Isolation": camp["isolation"],
            "Priority Score": round(score, 1),
            "Classification": level
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.sort_values(
            "Priority Score",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        df.sort_values("Priority Score"),
        x="Priority Score",
        y="Camp",
        orientation="h",
        text="Priority Score"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            family="Inter",
            size=12,
            color="#34424e"
        ),
        xaxis=dict(
            range=[0, 100],
            gridcolor="#e5e9ed"
        ),
        yaxis=dict(
            gridcolor="white"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SUPPLY ALLOCATION
# ============================================================

elif page == "Supply Allocation":

    st.markdown(
        '<div class="section-title">Supply Allocation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Proposed allocation of limited warehouse resources against camp requirements.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="alert-warning">
            <div class="alert-title">DECISION SUPPORT ONLY</div>
            <div class="alert-text">
                Allocation recommendations require coordinator review before deployment.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Generate Relief Allocation",
        type="primary"
    ):

        allocations, remaining = allocate_supplies(
            camps,
            warehouses
        )

        st.session_state.plan_generated = True

    if st.session_state.plan_generated:

        allocations, remaining = allocate_supplies(
            camps,
            warehouses
        )

        allocation_rows = []

        for item in allocations:

            allocation_rows.append({
                "Camp": item["camp"],
                "Warehouse": item["warehouse"],
                "Water": item.get("water", 0),
                "Food": item.get("food", 0),
                "Medical": item.get("medical", 0)
            })

        if allocation_rows:

            st.markdown(
                '<div class="section-title">Recommended Allocation Plan</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                pd.DataFrame(allocation_rows),
                use_container_width=True,
                hide_index=True
            )

        st.markdown(
            '<div class="section-title">Remaining Warehouse Inventory</div>',
            unsafe_allow_html=True
        )

        remaining_rows = []

        for warehouse, stock in remaining.items():

            remaining_rows.append({
                "Warehouse": warehouse,
                "Water": stock["water"],
                "Food": stock["food"],
                "Medical": stock["medical"]
            })

        st.dataframe(
            pd.DataFrame(remaining_rows),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ROUTE PLANNING
# ============================================================

elif page == "Route Planning":

    st.markdown(
        '<div class="section-title">Route Planning</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Flood-aware routing excludes roads marked as inaccessible in the simulation.
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_camp = st.selectbox(
        "Destination camp",
        [camp["name"] for camp in camps]
    )

    selected_warehouse = st.selectbox(
        "Dispatch warehouse",
        [warehouse["name"] for warehouse in warehouses]
    )

    if st.button(
        "Calculate Safe Route",
        type="primary"
    ):

        route, distance = find_route(
            selected_warehouse,
            selected_camp
        )

        if route:

            st.markdown(
                """
                <div class="alert-warning">
                    <div class="alert-title">ROUTE RECOMMENDATION</div>
                    <div class="alert-text">
                        Route generated using the simulated road network.
                        Confirm physical road conditions before deployment.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="panel">

                    <div class="panel-title">Recommended Route</div>

                    <div style="
                        font-family:'IBM Plex Mono';
                        font-size:13px;
                        color:#34424e;
                        line-height:2;
                    ">
                        {" → ".join(route)}
                    </div>

                    <div style="
                        margin-top:12px;
                        font-size:11px;
                        color:#71808b;
                    ">
                        Estimated route distance: <b>{distance}</b> km
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="alert-critical">
                    <div class="alert-title">NO SAFE ROUTE FOUND</div>
                    <div class="alert-text">
                        The simulated road network does not contain an available route.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# PERFORMANCE
# ============================================================

elif page == "Performance":

    st.markdown(
        '<div class="section-title">Evaluation Framework</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Example evaluation view. Values below are illustrative placeholders and are not experimental results.
        </div>
        """,
        unsafe_allow_html=True
    )

    comparison = pd.DataFrame({
        "Strategy": [
            "First-Come-First-Served",
            "Nearest Warehouse",
            "ReliefRoute"
        ],
        "Critical Demand Fulfilled (%)": [
            62,
            71,
            91
        ],
        "Camps Below Minimum": [
            7,
            5,
            2
        ],
        "Average Response Time (h)": [
            8.2,
            6.4,
            4.1
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="section-title">Recommended Evaluation Metrics</div>',
        unsafe_allow_html=True
    )

    metrics = [
        "Critical demand fulfilled",
        "Time to first delivery",
        "Number of camps below minimum supply",
        "Vulnerable-population coverage",
        "Total route distance",
        "Unmet demand",
        "Flooded-road violations"
    ]

    for metric in metrics:

        st.markdown(
            f"""
            <div style="
                background:white;
                border:1px solid #d8dde3;
                padding:9px 12px;
                margin-bottom:5px;
                font-size:12px;
                color:#45515b;
            ">
                {metric}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# HUMAN APPROVAL
# ============================================================

elif page == "Decision Approval":

    st.markdown(
        '<div class="section-title">Decision Approval</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
        Human coordinator remains responsible for approving operational recommendations.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="panel">

            <div class="panel-title">
                Relief Deployment Recommendation
            </div>

            <div style="
                display:grid;
                grid-template-columns:1fr 1fr;
                gap:10px;
                font-size:12px;
                color:#52616d;
            ">

                <div><b>Priority:</b> Critical camps first</div>
                <div><b>Allocation:</b> Warehouse stock constrained</div>
                <div><b>Routing:</b> Flooded roads excluded</div>
                <div><b>Minimum supply:</b> Enforced in prototype</div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="alert-warning">
            <div class="alert-title">REVIEW REQUIRED</div>
            <div class="alert-text">
                Verify field reports, road conditions, inventory and safety conditions before approving deployment.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Approve Recommendation",
            type="primary",
            use_container_width=True
        ):

            st.session_state.approved = True

    with col2:

        if st.button(
            "Request Reassessment",
            use_container_width=True
        ):

            st.session_state.approved = False
            st.warning(
                "Recommendation returned for coordinator reassessment."
            )

    if st.session_state.approved:

        st.success(
            "Recommendation marked APPROVED in the demonstration workflow."
        )

        st.markdown(
            """
            <div style="
                font-family:'IBM Plex Mono';
                font-size:11px;
                color:#52705d;
                margin-top:8px;
            ">
            STATUS: APPROVED — DEMONSTRATION ONLY
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <div>RELIEFROUTE AI • HUMANITARIAN LOGISTICS PROTOTYPE</div>
        <div class="mono">DEMO BUILD • NOT FOR LIVE DEPLOYMENT</div>
    </div>
    """,
    unsafe_allow_html=True
)
