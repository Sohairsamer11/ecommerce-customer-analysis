import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import textwrap 

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-commerce Customer Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# COLOR PALETTE
# =========================================================

NAVY = "#142F4B"
GOLD = "#C4A352"
LIGHT_BG = "#F7F8FA"
WHITE = "#FFFFFF"
TEXT = "#1F2937"
ORANGE = "#F2842F"


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv("ecommerce_customer_data.csv")

# Remove spaces from column names
df.columns = df.columns.str.strip()
# =========================================================
# STANDARDIZE CATEGORICAL VALUES
# =========================================================

df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})

df["IncomeLevel"] = df["IncomeLevel"].replace({
    "H": "High",
    "L": "Low"
})


# =========================================================
# CLEAN NUMERICAL COLUMNS
# =========================================================

numeric_columns = [
    "Age",
    "TotalPurchases",
    "AverageOrderValue",
    "CustomerLifetimeValue",
    "EmailEngagementRate",
    "SocialMediaEngagementRate",
    "CustomerServiceInteractions",
    "AverageSatisfactionScore",
    "EmailConversionRate",
    "SocialMediaConversionRate",
    "SearchEngineConversionRate"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# =========================================================
# CREATE CLEAN BINARY FLAGS
# =========================================================
# Keep the original Yes/No columns unchanged.
# These helper columns are used for calculations and filters.

df["RepeatCustomerFlag"] = (
    df["RepeatCustomer"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "yes": 1,
        "no": 0,
        "true": 1,
        "false": 0,
        "1": 1,
        "0": 0
    })
)

df["PremiumMemberFlag"] = (
    df["PremiumMember"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "yes": 1,
        "no": 0,
        "true": 1,
        "false": 0,
        "1": 1,
        "0": 0
    })
)

df["ReturnedItemsFlag"] = (
    df["HasReturnedItems"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "yes": 1,
        "no": 0,
        "true": 1,
        "false": 0,
        "1": 1,
        "0": 0
    })
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* Main application background */
    .stApp {{
        background-color: {LIGHT_BG};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {NAVY};
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    /* Main title */
    .main-title {{
        color: {NAVY};
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    /* Subtitle */
    .subtitle {{
        color: #64748B;
        font-size: 18px;
        margin-bottom: 30px;
    }}

    /* Section titles */
    .section-title {{
        color: {NAVY};
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }}

    /* Smooth scrolling for sidebar navigation */
    html, section.main, div[data-testid="stMain"],
    div[data-testid="stAppViewContainer"] {{
        scroll-behavior: smooth;
    }}

    .section-title {{
        scroll-margin-top: 20px;
    }}

    /* Sidebar navigation buttons */
    a.nav-link {{
        display: block;
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        padding: 10px 12px;
        margin: 10px 0;
        text-align: center;
        font-size: 15px;
        text-decoration: none !important;
        background-color: rgba(255, 255, 255, 0.05);
        transition: all 0.2s ease;
    }}

    a.nav-link:hover {{
        background-color: {ORANGE};
        border-color: {ORANGE};
        transform: translateX(3px);
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 5px;
        ">
            🛒 E-COMMERCE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            font-size: 15px;
            margin-bottom: 25px;
        ">
            Customer Analytics
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Sidebar menu items (label -> section anchor id)
    menu_items = {
        "🏠 Overview": "overview",
        "👥 Customer Analysis": "customer-analysis",
        "🌍 Geographic Analysis": "geographic-analysis",
        "📊 Customer Segmentation": "customer-segmentation",
        "💡 Key Insights": "key-insights"
    }

    for label, anchor in menu_items.items():
        st.markdown(
            f'<a class="nav-link" href="#{anchor}" target="_self">{label}</a>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            font-size: 15px;
            margin-top: 20px;
        ">
            Turning Customers into Opportunities
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    '<div class="main-title">E-commerce Customer Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Understand your customers. Drive smarter decisions.</div>',
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD FILTERS
# =========================================================

st.markdown(
    '<div class="section-title">Dashboard Filters</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


# -------------------------
# Country Filter
# -------------------------

with col1:

    country_filter = st.selectbox(
        "Country",
        ["All"] + sorted(
            df["Country"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )


# -------------------------
# Gender Filter
# -------------------------

with col2:

    gender_filter = st.selectbox(
        "Gender",
        ["All"] + sorted(
            df["Gender"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )


# -------------------------
# Income Filter
# -------------------------

with col3:

    income_filter = st.selectbox(
        "Income Level",
        ["All"] + sorted(
            df["IncomeLevel"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )


# -------------------------
# Customer Type Filter
# -------------------------

with col4:

    customer_type_filter = st.selectbox(
        "Customer Type",
        [
            "All",
            "Non-Repeat Customer",
            "Repeat Customer"
        ]
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


# -------------------------
# Country
# -------------------------

if country_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Country"].astype(str) == country_filter
    ]


# -------------------------
# Gender
# -------------------------

if gender_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Gender"].astype(str) == gender_filter
    ]


# -------------------------
# Income Level
# -------------------------

if income_filter != "All":

    filtered_df = filtered_df[
        filtered_df["IncomeLevel"].astype(str) == income_filter
    ]


# -------------------------
# Customer Type
# -------------------------

if customer_type_filter == "Non-Repeat Customer":

    filtered_df = filtered_df[
        filtered_df["RepeatCustomerFlag"] == 0
    ]

elif customer_type_filter == "Repeat Customer":

    filtered_df = filtered_df[
        filtered_df["RepeatCustomerFlag"] == 1
    ]


# =========================================================
# KEY PERFORMANCE INDICATORS
# =========================================================

st.markdown(
    '<div id="overview" class="section-title">Key Performance Indicators</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


# -------------------------
# Total Customers
# -------------------------

with col1:

    st.metric(
        "Total Customers",
        f"{len(filtered_df):,}"
    )


# -------------------------
# Average Order Value
# -------------------------

with col2:

    average_order_value = filtered_df[
        "AverageOrderValue"
    ].mean()

    if pd.isna(average_order_value):
        average_order_value = 0

    st.metric(
        "Average Order Value",
        f"{average_order_value:,.2f}"
    )


# -------------------------
# Total Purchases
# -------------------------

with col3:

    total_purchases = filtered_df[
        "TotalPurchases"
    ].sum()

    if pd.isna(total_purchases):
        total_purchases = 0

    st.metric(
        "Total Purchases",
        f"{total_purchases:,.0f}"
    )


# -------------------------
# Average Satisfaction
# -------------------------

with col4:

    average_satisfaction = filtered_df[
        "AverageSatisfactionScore"
    ].mean()

    if pd.isna(average_satisfaction):
        average_satisfaction = 0

    st.metric(
        "Average Satisfaction",
        f"{average_satisfaction:.2f}"
    )


# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

st.markdown(
    '<div id="customer-analysis" class="section-title">Customer Analysis</div>',
    unsafe_allow_html=True
)


# =========================================================
# ROW 1
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# CHART 1 — GENDER DISTRIBUTION
# =========================================================

with col1:

    gender_data = (
        filtered_df["Gender"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    gender_data.columns = [
        "Gender",
        "Customers"
    ]

    # Sort from smallest to largest
    gender_data = gender_data.sort_values("Customers", ascending=True)

    fig_gender = px.pie(
        gender_data,
        names="Gender",
        values="Customers",
        title="Customer Distribution by Gender",
        hole=0.55,
        color_discrete_sequence=[
    NAVY,
    "#F2842F",
    "#6F8FAF",
    "#E8B56A"
]
    )

    fig_gender.update_traces(
        sort=False,
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Customers: %{value:,}<br>"
            "Share: %{percent}<extra></extra>"
        )
    )

    fig_gender.update_layout(
        height=400,
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(color=NAVY),
        title_font=dict(
            size=18,
            color=NAVY
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )


# =========================================================
# CHART 2 — AGE DISTRIBUTION
# =========================================================

with col2:

    age_data = filtered_df[["Age"]].dropna().copy()

    # Create age groups
    age_data["Age Group"] = pd.cut(
        age_data["Age"],
        bins=[0, 18, 25, 35, 45, 55, 65, 100],
        labels=[
            "Under 18",
            "18–24",
            "25–34",
            "35–44",
            "45–54",
            "55–64",
            "65+"
        ],
        right=False
    )

    age_counts = (
        age_data["Age Group"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_counts.columns = ["Age Group", "Number of Customers"]

    # Sort from smallest to largest
    age_counts = age_counts.sort_values("Number of Customers", ascending=True)

    fig_age = px.bar(
        age_counts,
        x="Age Group",
        y="Number of Customers",
        title="Customer Age Distribution",
        color_discrete_sequence=["#F2842F"],
        text="Number of Customers"
    )

    fig_age.update_traces(
        textposition="outside",
        textfont=dict(
            color=NAVY,
            size=11
        ),
        hovertemplate=(
            "<b>Age Group:</b> %{x}<br>"
            "<b>Customers:</b> %{y}<extra></extra>"
        )
    )

    fig_age.update_layout(
        height=400,
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(color=NAVY),

        title_font=dict(
            size=18,
            color=NAVY
        ),

        xaxis_title="Age Group",
        yaxis_title="Number of Customers",

        showlegend=False,

        xaxis=dict(
            categoryorder="array",
            categoryarray=age_counts["Age Group"].astype(str).tolist(),
            tickangle=0
        ),

        margin=dict(
            l=60,
            r=20,
            t=60,
            b=60
        )
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True
    )

# =========================================================
# ROW 2
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# CHART 3 — PURCHASE BEHAVIOR
# =========================================================

with col1:

    behavior_data = (
        filtered_df[
            [
                "TotalPurchases",
                "AverageOrderValue"
            ]
        ]
        .dropna()
        .copy()
    )

    # Create purchase frequency groups
    behavior_data["Purchase Frequency"] = pd.cut(
        behavior_data["TotalPurchases"],
        bins=[-1, 2, 5, 10, 15, 20, float("inf")],
        labels=[
            "0–2 Purchases",
            "3–5 Purchases",
            "6–10 Purchases",
            "11–15 Purchases",
            "16–20 Purchases",
            "20+ Purchases"
        ]
    )

    # Calculate average order value for each group
    frequency_data = (
        behavior_data
        .groupby("Purchase Frequency", observed=False)["AverageOrderValue"]
        .mean()
        .reset_index()
    )

    frequency_data.columns = [
        "Purchase Frequency",
        "Average Order Value"
    ]

    # Keep the desired order
    frequency_data["Purchase Frequency"] = pd.Categorical(
        frequency_data["Purchase Frequency"],
        categories=[
            "0–2 Purchases",
            "3–5 Purchases",
            "6–10 Purchases",
            "11–15 Purchases",
            "16–20 Purchases",
            "20+ Purchases"
        ],
        ordered=True
    )

    frequency_data = frequency_data.sort_values(
        "Average Order Value",
        ascending=True
    )

    # Create horizontal bar chart
    fig_behavior = px.bar(
        frequency_data,
        x="Average Order Value",
        y="Purchase Frequency",
        orientation="h",
        title="Average Order Value by Purchase Frequency",
        color_discrete_sequence=["#F2842F"],
        text="Average Order Value"
    )

    # Data labels
    fig_behavior.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont=dict(
            color=NAVY,
            size=11
        ),
        cliponaxis=False,
        hovertemplate=(
            "<b>Purchase Frequency:</b> %{y}<br>"
            "<b>Average Order Value:</b> %{x:.2f}"
            "<extra></extra>"
        )
    )

    # Find maximum value to create extra space for labels
    max_value = frequency_data["Average Order Value"].max()

    fig_behavior.update_layout(
        height=400,
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(color=NAVY),

        title_font=dict(
            size=18,
            color=NAVY
        ),

        xaxis_title="Average Order Value",
        yaxis_title="Purchase Frequency",

        showlegend=False,

        # Extra space around the chart
        margin=dict(
            l=120,
            r=80,
            t=60,
            b=60
        ),

        # Give labels enough room on the right
        xaxis=dict(
            range=[0, max_value * 1.18]
        )
    )

    st.plotly_chart(
        fig_behavior,
        use_container_width=True
    )


    
# =========================================================
# CHART 4 — CUSTOMER ENGAGEMENT
# =========================================================

# =========================================================
# CHART 4 — CUSTOMER ENGAGEMENT
# =========================================================

with col2:

    engagement_data = filtered_df[
        [
            "EmailEngagementRate",
            "SocialMediaEngagementRate"
        ]
    ].mean().reset_index()

    engagement_data.columns = [
        "Metric",
        "Average"
    ]

    engagement_data["Metric"] = [
        "Email Engagement",
        "Social Media Engagement"
    ]

    # Sort from smallest to largest
    engagement_data = engagement_data.sort_values("Average", ascending=True)

    fig_engagement = px.pie(
        engagement_data,
        names="Metric",
        values="Average",
        title="Customer Engagement by Channel",
        hole=0.55,
        color_discrete_sequence=[
            NAVY,
            "#F2842F"
        ]
    )

    fig_engagement.update_traces(
        sort=False,
        textposition="inside",
        texttemplate="%{percent:.1%}",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Average Engagement: %{value:.2f}<br>"
            "Share: %{percent}<extra></extra>"
        ),
        marker=dict(
            line=dict(
                color=WHITE,
                width=2
            )
        )
    )

    fig_engagement.update_layout(
        height=400,
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(
            color=NAVY
        ),
        title_font=dict(
            size=18,
            color=NAVY
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=70
        )
    )

    st.plotly_chart(
        fig_engagement,
        use_container_width=True
    )
# =========================================================
# MOBILE APP USAGE + CUSTOMER EXPERIENCE
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# CHART 5 — MOBILE APP USAGE
# =========================================================

with col1:

    st.markdown(
        '<div class="section-title">Mobile App Usage</div>',
        unsafe_allow_html=True
    )

    mobile_data = (
        filtered_df["MobileAppUsage"]
        .value_counts()
        .reindex(
            ["Never", "Low", "Medium", "High"],
            fill_value=0
        )
        .reset_index()
    )

    mobile_data.columns = [
        "Usage Level",
        "Customers"
    ]

    # Sort from smallest to largest
    mobile_data = mobile_data.sort_values("Customers", ascending=True)

    fig_mobile = px.bar(
        mobile_data,
        x="Customers",
        y="Usage Level",
        orientation="h",
        color_discrete_sequence=["#F2842F"],
        text="Customers"
    )

    fig_mobile.update_traces(
        width=0.60,
        textposition="outside",
        cliponaxis=False,

        texttemplate="%{x:,}",

        textfont=dict(
            color=NAVY,
            size=11
        ),

        hovertemplate=(
            "<b>Mobile App Usage:</b> %{y}<br>"
            "<b>Customers:</b> %{x:,}"
            "<extra></extra>"
        )
    )

    fig_mobile.update_layout(
        height=380,

        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,

        font=dict(
            color=NAVY,
            size=11
        ),

        xaxis=dict(
            title="Number of Customers",
            title_font=dict(size=12),
            tickfont=dict(size=10),
            showgrid=True,
            gridcolor="#D9E4F0",
            zeroline=False
        ),

        yaxis=dict(
            title="Mobile App Usage",
            title_font=dict(size=12),
            tickfont=dict(size=10),
            showgrid=False
        ),

        showlegend=False,

        margin=dict(
            l=90,
            r=55,
            t=25,
            b=55
        )
    )

    st.plotly_chart(
        fig_mobile,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True
        }
    )


# =========================================================
# CHART 6 — CUSTOMER EXPERIENCE
# =========================================================

with col2:

    st.markdown(
        '<div class="section-title">Customer Experience</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Prepare satisfaction data
    # -----------------------------------------------------

    satisfaction_data = (
        filtered_df["AverageSatisfactionScore"]
        .dropna()
    )

    # -----------------------------------------------------
    # Create fixed 1-point satisfaction bins
    # -----------------------------------------------------

    satisfaction_bins = pd.cut(
        satisfaction_data,
        bins=list(range(0, 11)),
        right=False,
        include_lowest=True
    )

    satisfaction_counts = (
        satisfaction_bins
        .value_counts()
        .sort_index()
        .reset_index()
    )

    satisfaction_counts.columns = [
        "Satisfaction Range",
        "Customers"
    ]

    # -----------------------------------------------------
    # Create readable labels
    # -----------------------------------------------------

    satisfaction_counts["Satisfaction Range"] = [
        f"{int(interval.left)}–{int(interval.right)}"
        for interval in satisfaction_counts["Satisfaction Range"]
    ]

    # Sort from smallest to largest
    satisfaction_counts = satisfaction_counts.sort_values(
        "Customers",
        ascending=True
    )

    # -----------------------------------------------------
    # Satisfaction bar chart
    # -----------------------------------------------------

    fig_satisfaction = px.bar(
        satisfaction_counts,
        x="Satisfaction Range",
        y="Customers",
        color_discrete_sequence=[NAVY],
        text="Customers"
    )

    fig_satisfaction.update_traces(
        textposition="outside",
        cliponaxis=False,

        texttemplate="%{y:,}",

        textfont=dict(
            color=NAVY,
            size=10
        ),

        hovertemplate=(
            "<b>Satisfaction Range:</b> %{x}<br>"
            "<b>Customers:</b> %{y:,}"
            "<extra></extra>"
        )
    )

    fig_satisfaction.update_layout(
        height=380,

        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,

        font=dict(
            color=NAVY,
            size=11
        ),

        xaxis=dict(
            title="Average Satisfaction Score",
            title_font=dict(size=12),
            tickfont=dict(size=9),
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            title="Number of Customers",
            title_font=dict(size=12),
            tickfont=dict(size=10),
            showgrid=True,
            gridcolor="#D9E4F0",
            zeroline=False
        ),

        showlegend=False,

        # Space between bars
        bargap=0.18,

        margin=dict(
            l=60,
            r=35,
            t=25,
            b=60
        )
    )

    st.plotly_chart(
        fig_satisfaction,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True
        }
    )
# =========================================================
# GEOGRAPHIC ANALYSIS
# =========================================================

st.markdown(
    '<div id="geographic-analysis" class="section-title">Geographic Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)    

# =========================================================
# GEOGRAPHIC ANALYSIS
# =========================================================

# =========================================================
# CHART — TOP 10 COUNTRIES BY CUSTOMERS
# =========================================================
with col1:

    if country_filter == "All":

        # =====================================================
        # ALL COUNTRIES → TOP 10 HORIZONTAL BAR CHART
        # =====================================================

        country_data = (
            filtered_df["Country"]
            .dropna()
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
            .reset_index()
        )

        country_data.columns = [
            "Country",
            "Customers"
        ]

        fig_country = px.bar(
            country_data,
            x="Customers",
            y="Country",
            orientation="h",
            title="Top 10 Countries by Customers",
            color_discrete_sequence=["#F2842F"],
            text="Customers"
        )

        fig_country.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig_country.update_layout(
            height=400,
            plot_bgcolor=WHITE,
            paper_bgcolor=WHITE,
            font=dict(color=NAVY),

            title_font=dict(
                size=18,
                color=NAVY
            ),

            xaxis_title="Number of Customers",
            yaxis_title="Country",
            yaxis=dict(
                categoryorder="total ascending"
            ),

            showlegend=False,

            margin=dict(
                l=70,
                r=70,
                t=60,
                b=60
            )
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    else:

        # =====================================================
        # SPECIFIC COUNTRY → KPI INDICATOR
        # =====================================================

        selected_country_count = len(filtered_df)

        import plotly.graph_objects as go

        fig_country = go.Figure()

        fig_country.add_trace(
            go.Indicator(
                mode="number",
                value=selected_country_count,
                number={
                    "font": {
                        "size": 52,
                        "color": NAVY
                    },
                    "valueformat": ","
                },
                title={
                    "text": (
                        f"<b>Customers in {country_filter}</b>"
                        "<br>"
                        "<span style='font-size:16px; color:#F2842F;'>"
                        "Total Customers"
                        "</span>"
                    ),
                    "font": {
                        "size": 18,
                        "color": NAVY
                    }
                }
            )
        )

        fig_country.update_layout(
            height=400,
            plot_bgcolor=WHITE,
            paper_bgcolor=WHITE,

            margin=dict(
                l=30,
                r=30,
                t=80,
                b=30
            )
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )
# =========================================================
# CHART 6 — INCOME LEVEL
# =========================================================
# =========================================================
# CHART — CUSTOMER BY INCOME LEVEL
# =========================================================

with col2:

    income_data = filtered_df[["IncomeLevel"]].dropna().copy()

    # =====================================================
    # STANDARDIZE INCOME LEVEL CATEGORIES
    # =====================================================

    income_data["Income Level"] = income_data["IncomeLevel"].replace({
        "L": "Low",
        "H": "High"
    })

    # =====================================================
    # COUNT CUSTOMERS
    # =====================================================

    income_data = (
        income_data["Income Level"]
        .value_counts()
        .reset_index()
    )

    income_data.columns = [
        "Income Level",
        "Customers"
    ]

    # =====================================================
    # KEEP ONLY VALID INCOME LEVELS
    # =====================================================

    income_order = [
        "Low",
        "Medium",
        "High",
        "Very High"
    ]

    income_data = income_data[
        income_data["Income Level"].isin(income_order)
    ]

    income_data["Income Level"] = pd.Categorical(
        income_data["Income Level"],
        categories=income_order,
        ordered=True
    )

    income_data = income_data.sort_values(
        "Customers",
        ascending=True
    )

    # =====================================================
    # CREATE LOLLIPOP CHART
    # =====================================================

    fig_income = go.Figure()

    # =====================================================
    # NAVY LINES
    # =====================================================

    for _, row in income_data.iterrows():

        fig_income.add_trace(
            go.Scatter(
                x=[0, row["Customers"]],
                y=[
                    row["Income Level"],
                    row["Income Level"]
                ],

                mode="lines",

                line=dict(
                    color=NAVY,
                    width=4
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )

    # =====================================================
    # ORANGE POINTS
    # =====================================================

    fig_income.add_trace(
        go.Scatter(
            x=income_data["Customers"],
            y=income_data["Income Level"],

            mode="markers+text",

            text=income_data["Customers"],
            textposition="middle right",

            marker=dict(
                size=16,
                color="#F2842F"
            ),

            textfont=dict(
                color=NAVY,
                size=11
            ),

            hovertemplate=(
                "<b>Income Level:</b> %{y}<br>"
                "<b>Customers:</b> %{x:,}"
                "<extra></extra>"
            ),

            showlegend=False
        )
    )

    # =====================================================
    # LAYOUT
    # =====================================================

    fig_income.update_layout(
        height=400,

        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,

        font=dict(
            color=NAVY
        ),

        title=dict(
            text="Customer Distribution by Income Level",
            font=dict(
                size=18,
                color=NAVY
            )
        ),

        xaxis=dict(
            title="Number of Customers",
            showgrid=True,
            gridcolor="#E5E5E5",
            zeroline=False
        ),

        yaxis=dict(
            title="Income Level",
            showgrid=False,

            categoryorder="array",
            categoryarray=income_data["Income Level"].astype(str).tolist()
        ),

        showlegend=False,

        margin=dict(
            l=70,
            r=80,
            t=60,
            b=60
        )
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    st.plotly_chart(
        fig_income,
        use_container_width=True
    )
# =========================================================
# CUSTOMER SEGMENTATION
# =========================================================

st.markdown(
    '<div id="customer-segmentation" class="section-title">Customer Segmentation</div>',
    unsafe_allow_html=True
)

# =========================================================
# COLORS
# =========================================================

ORANGE = "#F2842F"
LIGHT_BLUE = "#F3F7FC"
LIGHT_ORANGE = "#FFF7EE"
BORDER_BLUE = "#D9E4F0"
BORDER_ORANGE = "#F5D8B8"
NAVY = "#142F4B"
TEXT_GRAY = "#506784"


# =========================================================
# CALCULATE SEGMENTS
# =========================================================

new_customers = (filtered_df["RepeatCustomerFlag"] == 0).sum()
repeat_customers = (filtered_df["RepeatCustomerFlag"] == 1).sum()

premium_customers = (filtered_df["PremiumMemberFlag"] == 1).sum()
non_premium_customers = (filtered_df["PremiumMemberFlag"] == 0).sum()

total_repeat_customers = new_customers + repeat_customers
total_membership_customers = premium_customers + non_premium_customers

new_percentage = (
    new_customers / total_repeat_customers * 100
    if total_repeat_customers > 0 else 0
)

repeat_percentage = (
    repeat_customers / total_repeat_customers * 100
    if total_repeat_customers > 0 else 0
)

premium_percentage = (
    premium_customers / total_membership_customers * 100
    if total_membership_customers > 0 else 0
)

non_premium_percentage = (
    non_premium_customers / total_membership_customers * 100
    if total_membership_customers > 0 else 0
)


# =========================================================
# CARD STYLE
# =========================================================

st.markdown(
    """
    <style>

    .segment-card {
        border-radius: 14px;
        padding: 14px 16px;
        height: 125px;
        margin-bottom: 16px;
        box-sizing: border-box;
    }

    .segment-card-blue {
        background-color: #F3F7FC;
        border: 1px solid #D9E4F0;
    }

    .segment-card-orange {
        background-color: #FFF7EE;
        border: 1px solid #F5D8B8;
    }

    .segment-label {
        font-size: 14px;
        color: #506784;
        margin-bottom: 7px;
    }

    .segment-value {
        font-size: 28px;
        font-weight: 700;
        color: #142F4B;
        line-height: 1.1;
    }

    .segment-percent {
        font-size: 13px;
        margin-top: 6px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TWO MAIN COLUMNS
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# LEFT SIDE
# =========================================================

with col1:

    st.markdown(
        f"""
        <h3 style="
            color: {NAVY};
            font-size: 18px;
            margin-bottom: 14px;
        ">
        Non-Repeat vs Repeat Customers
        </h3>
        """,
        unsafe_allow_html=True
    )

    card1, card2 = st.columns(2)

    # -----------------------------------------------------
    # NEW CUSTOMERS
    # -----------------------------------------------------

    with card1:

        st.markdown(
            f"""
            <div class="segment-card segment-card-blue">
                <div class="segment-label">👤 Non-Repeat Customers</div>
                <div class="segment-value">{new_customers:,}</div>
                <div class="segment-percent" style="color:{TEXT_GRAY};">
                    {new_percentage:.1f}% of valid Customer records
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # REPEAT CUSTOMERS
    # -----------------------------------------------------

    with card2:

        st.markdown(
            f"""
            <div class="segment-card segment-card-orange">
                <div class="segment-label">👥 Repeat Customers</div>
                <div class="segment-value">{repeat_customers:,}</div>
                <div class="segment-percent" style="color:{ORANGE};">
                    {repeat_percentage:.1f}% of valid Customer records
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # CHART
    # -----------------------------------------------------

    segmentation_data = pd.DataFrame({
        "Customer Type": [
            "Non-Repeat Customer",
            "Repeat Customer"
        ],
        "Customers": [
            new_customers,
            repeat_customers
        ]
    })

    segmentation_data = segmentation_data.sort_values("Customers", ascending=True)

    fig_segmentation = px.bar(
        segmentation_data,
        x="Customers",
        y="Customer Type",
        orientation="h",
        text="Customers",
        color="Customer Type",
        color_discrete_map={
            "Non-Repeat Customer": NAVY,
            "Repeat Customer": ORANGE
        }
    )

    fig_segmentation.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Customers: %{x:,}"
            "<extra></extra>"
        )
    )

    fig_segmentation.update_layout(
        title="Non-Repeat vs Repeat Customers",
        height=270,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=NAVY),
        title_font=dict(
            size=17,
            color=NAVY
        ),
        xaxis_title="Number of Customers",
        yaxis_title="",
        showlegend=False,
        margin=dict(
            l=20,
            r=55,
            t=50,
            b=45
        )
    )

    fig_segmentation.update_xaxes(
        showgrid=True,
        gridcolor=BORDER_BLUE,
        zeroline=False
    )

    fig_segmentation.update_yaxes(
        showgrid=False
    )

    st.plotly_chart(
        fig_segmentation,
        use_container_width=True
    )


# =========================================================
# RIGHT SIDE
# =========================================================

with col2:

    st.markdown(
        f"""
        <h3 style="
            color: {NAVY};
            font-size: 18px;
            margin-bottom: 14px;
        ">
        Premium Membership Distribution
        </h3>
        """,
        unsafe_allow_html=True
    )

    card3, card4 = st.columns(2)

    # -----------------------------------------------------
    # PREMIUM MEMBERS
    # -----------------------------------------------------

    with card3:

        st.markdown(
            f"""
            <div class="segment-card segment-card-orange">
                <div class="segment-label">👑 Premium Members</div>
                <div class="segment-value">{premium_customers:,}</div>
                <div class="segment-percent" style="color:{ORANGE};">
                    {premium_percentage:.1f}% of valid  Customer records 
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # NON PREMIUM
    # -----------------------------------------------------

    with card4:

        st.markdown(
            f"""
            <div class="segment-card segment-card-blue">
                <div class="segment-label">👥 Non-Premium</div>
                <div class="segment-value">{non_premium_customers:,}</div>
                <div class="segment-percent" style="color:{TEXT_GRAY};">
                    {non_premium_percentage:.1f}% of valid Customer records
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # CHART
    # -----------------------------------------------------

    premium_data = pd.DataFrame({
        "Membership": [
            "Premium Member",
            "Non-Premium"
        ],
        "Customers": [
            premium_customers,
            non_premium_customers
        ]
    })

    premium_data = premium_data.sort_values("Customers", ascending=True)

    fig_premium = px.bar(
        premium_data,
        x="Customers",
        y="Membership",
        orientation="h",
        text="Customers",
        color="Membership",
        color_discrete_map={
            "Premium Member": ORANGE,
            "Non-Premium": NAVY
        }
    )

    fig_premium.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Customers: %{x:,}"
            "<extra></extra>"
        )
    )

    fig_premium.update_layout(
        title="Premium vs Non-Premium",
        height=270,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=NAVY),
        title_font=dict(
            size=17,
            color=NAVY
        ),
        xaxis_title="Number of Customers",
        yaxis_title="",
        showlegend=False,
        margin=dict(
            l=20,
            r=55,
            t=50,
            b=45
        )
    )

    fig_premium.update_xaxes(
        showgrid=True,
        gridcolor=BORDER_BLUE,
        zeroline=False
    )

    fig_premium.update_yaxes(
        showgrid=False
    )

    st.plotly_chart(
        fig_premium,
        use_container_width=True
    )


# =========================================================
# KEY INSIGHT
# =========================================================

st.markdown(
    f"""
    <div style="
        background-color:#F0F6FD;
        border:1px solid #E0EBF6;
        border-radius:14px;
        padding:16px 22px;
        margin-top:18px;
        margin-bottom:20px;
        color:#142F4B;
        font-size:15px;
    ">
        💡 <b>Insight:</b>
        {repeat_percentage:.1f}% of valid customers records are repeat customers,
        and {premium_percentage:.1f}% of valid customer records are premium members.
    </div>
    """,
    unsafe_allow_html=True
)
# =========================================================
# KEY BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div id="key-insights" class="section-title">Key Business Insights</div>',
    unsafe_allow_html=True
)


# =========================================================
# CALCULATE BUSINESS METRICS
# =========================================================

total_customers = len(filtered_df)

repeat_valid = filtered_df[
    "RepeatCustomerFlag"
].notna().sum()

premium_valid = filtered_df[
    "PremiumMemberFlag"
].notna().sum()

returned_valid = filtered_df[
    "ReturnedItemsFlag"
].notna().sum()


# -------------------------
# Repeat Customer Rate
# -------------------------

if repeat_valid > 0:

    repeat_rate = (
        filtered_df["RepeatCustomerFlag"].sum()
        / repeat_valid
    ) * 100

else:

    repeat_rate = 0


# -------------------------
# Premium Customer Rate
# -------------------------

if premium_valid > 0:

    premium_rate = (
        filtered_df["PremiumMemberFlag"].sum()
        / premium_valid
    ) * 100

else:

    premium_rate = 0


# -------------------------
# Return Rate
# -------------------------

if returned_valid > 0:

    return_rate = (
        filtered_df["ReturnedItemsFlag"].sum()
        / returned_valid
    ) * 100

else:

    return_rate = 0


# -------------------------
# Average CLV
# -------------------------

average_clv = filtered_df[
    "CustomerLifetimeValue"
].mean()

if pd.isna(average_clv):

    average_clv = 0


# =========================================================
# BUSINESS INSIGHT CARDS
# =========================================================

col1, col2, col3 = st.columns(3)


# =========================================================
# CARD 1 — REPEAT CUSTOMER RATE
# =========================================================

with col1:

    st.markdown(
        f"""
        <div style="
            background-color:#E5F0FA;
            padding:20px;
            border-radius:6px;
            min-height:135px;
        ">

        <h4 style="color:{NAVY};">
        Repeat Customer Rate
        </h4>

        <p style="
            color:{TEXT};
            font-size:16px;
        ">

        <b>{repeat_rate:.1f}%</b> of valid customer
        records are classified as repeat customers.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CARD 2 — PREMIUM CUSTOMER RATE
# =========================================================

with col2:

    st.markdown(
        f"""
        <div style="
            background-color:#E5F0FA;
            padding:20px;
            border-radius:6px;
            min-height:135px;
        ">

        <h4 style="color:{NAVY};">
        Premium Customer Rate
        </h4>

        <p style="
            color:{TEXT};
            font-size:16px;
        ">

        <b>{premium_rate:.1f}%</b> of valid customer
        records are premium members.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CARD 3 — RETURN RATE
# =========================================================

with col3:

    st.markdown(
        f"""
        <div style="
            background-color:#E5F0FA;
            padding:20px;
            border-radius:6px;
            min-height:135px;
        ">

        <h4 style="color:{NAVY};">
        Return Rate
        </h4>

        <p style="
            color:{TEXT};
            font-size:16px;
        ">

        <b>{return_rate:.1f}%</b> of valid customer
        records have returned items.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SECOND ROW OF BUSINESS INSIGHTS
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# AVERAGE CUSTOMER LIFETIME VALUE
# =========================================================

with col1:

    st.markdown(
        f"""
        <div style="
            background-color:#E5F0FA;
            padding:20px;
            border-radius:6px;
            min-height:135px;
            margin-top:15px;
        ">

        <h4 style="color:{NAVY};">
        Average Customer Lifetime Value
        </h4>

        <p style="
            color:{TEXT};
            font-size:16px;
        ">

        The average customer lifetime value is
        <b>{average_clv:,.2f}</b>.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CUSTOMER BASE
# =========================================================

with col2:

    st.markdown(
        f"""
        <div style="
            background-color:#E5F0FA;
            padding:20px;
            border-radius:6px;
            min-height:135px;
            margin-top:15px;
        ">

        <h4 style="color:{NAVY};">
        Customer Base
        </h4>

        <p style="
            color:{TEXT};
            font-size:16px;
        ">

        The dashboard currently includes
        <b>{total_customers:,}</b> customers
        after applying the selected filters.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
