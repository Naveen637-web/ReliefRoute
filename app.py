import streamlit as st
import pandas as pd
import plotly.express as px

from data import get_camps, get_warehouses
from scoring import add_priority_scores
from allocation import allocate_supplies
from routing import find_route


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="ReliefRoute AI",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: #08111f;
}

[data-testid="stSidebar"] {
    background-color: #0d1b2a;
}

h1, h2, h3 {
    color: #ffffff;
}

p, label {
    color: #d9e2ec;
}

.metric-card {
    background-color: #101f33;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #243b53;
}

.priority-critical {
    background-color: #4a1515;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #ff4b4b;
}

.priority-high {
    background-color: #4a3515;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #ffa500;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

camps = get_camps()
warehouses = get_warehouses()

scored_camps = add_priority_scores(camps)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚑 ReliefRoute AI")

st.sidebar.caption(
    "Emergency relief decision-support prototype"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "COMMAND CENTER",
    [
        "Dashboard",
        "Field Reports",
        "Priority Engine",
        "Supply Allocation",
        "Route Planner",
        "Performance",
        "Human Approval"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Prototype mode\n\n"
    "Data shown here is simulated for demonstration."
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("🚑 ReliefRoute AI")

    st.subheader(
        "Emergency Relief Command Center"
    )

    st.caption(
        "Helping coordinators decide which camp gets what, "
        "from where, and by which route."
    )

    st.divider()

    # METRICS

    col1, col2, col3, col4, col5 = st.columns(5)

    critical = sum(
        scored_camps["Priority Score"] >= 80
    )

    total_people = camps["People"].sum()

    total_water = warehouses["Water"].sum()

    total_food = warehouses["Food"].sum()

    col1.metric(
        "Relief Camps",
        len(camps)
    )

    col2.metric(
        "People Affected",
        f"{total_people:,}"
    )

    col3.metric(
        "Critical Camps",
        critical
    )

    col4.metric(
        "Water Available",
        f"{total_water:,} L"
    )

    col5.metric(
        "Food Available",
        f"{total_food:,} kg"
    )

    st.divider()

    # ALERT

    highest = scored_camps.sort_values(
        "Priority Score",
        ascending=False
    ).iloc[0]

    st.markdown(
        f"""
        <div class="priority-critical">

        🚨 <b>HIGHEST PRIORITY CAMP</b>

        <br><br>

        <b>{highest['Camp']}</b>

        — Priority Score: <b>{highest['Priority Score']}</b>

        <br>

        Health Risk: {highest['Health Risk']}/100 |
        Vulnerability: {highest['Vulnerable']}/100 |
        Time Without Aid: {highest['Time Without Aid']} hours |
        Isolation: {highest['Isolation']}/100

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # CHART

    st.subheader("Camp Priority")

    chart_data = scored_camps.sort_values(
        "Priority Score",
        ascending=True
    )

    fig = px.bar(
        chart_data,
        x="Priority Score",
        y="Camp",
        orientation="h",
        text="Priority Score",
        range_x=[0, 100]
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Priority Score",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FIELD REPORTS
# ============================================================

elif page == "Field Reports":

    st.title("📱 Field Reports")

    st.caption(
        "Incoming reports from volunteers and field coordinators"
    )

    reports = [
        (
            "Camp 1",
            "08:42",
            "350 people. Water supplies decreasing. "
            "No major health problems reported."
        ),
        (
            "Camp 2",
            "09:05",
            "520 people. Water critically low. "
            "Several vulnerable residents. "
            "No delivery for 24 hours."
        ),
        (
            "Camp 3",
            "09:17",
            "280 people. Food needed. "
            "Road access currently available."
        ),
        (
            "Camp 4",
            "09:31",
            "610 people. Critical food and water shortage. "
            "Health concerns reported. Main road flooded. "
            "No supplies for 23 hours."
        ),
        (
            "Camp 5",
            "09:48",
            "430 people. Moderate water shortage. "
            "Some vulnerable residents."
        )
    ]

    for camp, time, message in reports:

        with st.container(border=True):

            col1, col2 = st.columns([1, 5])

            with col1:
                st.caption(time)
                st.markdown(f"### {camp}")

            with col2:
                st.write(message)

                if st.button(
                    f"Analyze {camp}",
                    key=f"analyze_{camp}"
                ):

                    camp_data = scored_camps[
                        scored_camps["Camp"] == camp
                    ].iloc[0]

                    st.success(
                        "Report converted into structured data."
                    )

                    st.json({
                        "camp": camp,
                        "people": int(camp_data["People"]),
                        "health_risk": int(
                            camp_data["Health Risk"]
                        ),
                        "vulnerable_population": int(
                            camp_data["Vulnerable"]
                        ),
                        "hours_without_aid": int(
                            camp_data["Time Without Aid"]
                        ),
                        "isolation": int(
                            camp_data["Isolation"]
                        )
                    })


# ============================================================
# PRIORITY ENGINE
# ============================================================

elif page == "Priority Engine":

    st.title("🧠 Explainable Priority Engine")

    st.markdown(
        """
        ReliefRoute does not simply prioritize the camp that
        sends the most messages.

        The prototype combines four documented factors:
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Health Risk", "35%")
    c2.metric("Vulnerability", "25%")
    c3.metric("Time Without Aid", "25%")
    c4.metric("Isolation", "15%")

    st.divider()

    st.code(
        """
Priority Score =
    0.35 × Health Risk
  + 0.25 × Vulnerability
  + 0.25 × Time Without Aid
  + 0.15 × Isolation
        """
    )

    display = scored_camps[
        [
            "Camp",
            "Health Risk",
            "Vulnerable",
            "Time Without Aid",
            "Isolation",
            "Priority Score",
            "Priority Level"
        ]
    ].sort_values(
        "Priority Score",
        ascending=False
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected = st.selectbox(
        "Inspect a camp",
        scored_camps["Camp"]
    )

    camp = scored_camps[
        scored_camps["Camp"] == selected
    ].iloc[0]

    st.subheader(
        f"{selected} — Score {camp['Priority Score']}"
    )

    factors = pd.DataFrame({
        "Factor": [
            "Health Risk",
            "Vulnerability",
            "Time Without Aid",
            "Isolation"
        ],
        "Score": [
            camp["Health Risk"],
            camp["Vulnerable"],
            min(
                camp["Time Without Aid"] / 24 * 100,
                100
            ),
            camp["Isolation"]
        ]
    })

    fig = px.bar(
        factors,
        x="Factor",
        y="Score",
        range_y=[0, 100],
        text="Score"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SUPPLY ALLOCATION
# ============================================================

elif page == "Supply Allocation":

    st.title("📦 Supply Allocation")

    st.caption(
        "Allocate limited stock according to camp priority."
    )

    if st.button(
        "⚡ Generate Relief Plan",
        type="primary"
    ):

        allocations, remaining = allocate_supplies(
            scored_camps,
            warehouses
        )

        allocation_df = pd.DataFrame(
            allocations
        )

        st.session_state["allocations"] = allocation_df

        st.success(
            "Relief plan generated."
        )

    if "allocations" in st.session_state:

        allocation_df = st.session_state[
            "allocations"
        ]

        st.subheader("Recommended Deliveries")

        st.dataframe(
            allocation_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader(
            "⚠️ Human approval required"
        )

        st.warning(
            "The system recommends an allocation. "
            "It does not authorize deployment."
        )


# ============================================================
# ROUTE PLANNER
# ============================================================

elif page == "Route Planner":

    st.title("🚚 Flood-Aware Route Planner")

    st.write(
        "Routes marked as flooded are automatically excluded."
    )

    col1, col2 = st.columns(2)

    with col1:

        warehouse = st.selectbox(
            "Warehouse",
            warehouses["Warehouse"]
        )

    with col2:

        camp = st.selectbox(
            "Destination Camp",
            camps["Camp"]
        )

    if st.button(
        "🗺️ Calculate Safe Route",
        type="primary"
    ):

        route, distance = find_route(
            warehouse,
            camp
        )

        if route:

            st.success(
                "SAFE ROUTE FOUND"
            )

            st.markdown(
                "### " +
                " → ".join(route)
            )

            st.metric(
                "Estimated Distance",
                f"{distance} km"
            )

            st.info(
                "Flooded roads were excluded "
                "from route selection."
            )

        else:

            st.error(
                "No safe route currently available."
            )


# ============================================================
# PERFORMANCE
# ============================================================

elif page == "Performance":

    st.title("📊 Strategy Comparison")

    st.caption(
        "Illustrative prototype comparison — "
        "replace these values with results from the "
        "real simulation before presenting them as findings."
    )

    comparison = pd.DataFrame({
        "Strategy": [
            "First-Come-First-Served",
            "Nearest Warehouse",
            "ReliefRoute AI"
        ],
        "Critical Demand Fulfilled": [
            62,
            71,
            91
        ],
        "Camps Below Minimum": [
            7,
            5,
            2
        ],
        "Average Response Time": [
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

    st.divider()

    fig = px.bar(
        comparison,
        x="Strategy",
        y="Critical Demand Fulfilled",
        text="Critical Demand Fulfilled",
        range_y=[0, 100]
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis_title="% Critical Demand Fulfilled"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning(
        "These numbers are demonstration values. "
        "Do not use them as experimental results."
    )


# ============================================================
# HUMAN APPROVAL
# ============================================================

elif page == "Human Approval":

    st.title("👨‍💼 Human Coordinator")

    st.warning(
        "AI recommendation — awaiting human authorization"
    )

    st.divider()

    st.subheader(
        "Recommended Action"
    )

    st.markdown(
        """
        ### 🚨 Prioritize Camp 4

        **Reason**

        • High health risk  
        • Large vulnerable population  
        • 23 hours without aid  
        • High isolation  
        • Critical water requirement  
        • Critical food requirement
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ APPROVE",
            type="primary",
            use_container_width=True
        ):

            st.success(
                "Recommendation approved by coordinator."
            )

            st.session_state[
                "approved"
            ] = True

    with col2:

        if st.button(
            "❌ REJECT / MODIFY",
            use_container_width=True
        ):

            st.warning(
                "Recommendation returned for review."
            )

    if st.session_state.get(
        "approved",
        False
    ):

        st.success(
            "🚚 Relief operation authorized."
        )
