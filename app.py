import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from PIL import Image

# =============================
# PLOTLY GLOBAL STYLE
# =============================
PLOTLY_LAYOUT = dict(
    height=420,
    margin=dict(l=40, r=40, t=60, b=40),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Segoe UI",
        size=13,
        color="#1e293b"
    ),
    title=dict(
        font=dict(size=18, color="#15264d")
    )
)

COLOR_PALETTE = [
    "#5b5dd8",
    "#6366f1",
    "#7dd3fc",
    "#22c55e",
    "#f59e0b",
    "#ef4444"
]

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Bike Sales in Europe",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# CUSTOM STYLE
# =============================
st.markdown("""
<style>
/* ===============================
GLOBAL APP
=============================== */
.stApp {
    background: linear-gradient(135deg, #5b5dd8, #cad5f9,#abcaf7);
    font-family: 'Segoe UI', sans-serif;
    color: #1e293b;
}
.block-container {
    padding: 2.5rem 3rem;
}

/* ===============================
SIDEBAR
=============================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(120deg, #5b5dd8,#6062f0, #a19df7);
    box-shadow: 8px 0 30px rgba(79,70,229,0.35);
}
section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 500;
}

/* ===============================
HEADER
=============================== */
.header {
    background: linear-gradient(90deg, #6365e8, #8498ff,#97a8ff, #7dd3fc);
    padding: 35px;
    border-radius: 28px;
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 20px;
    color: #15264d;
    box-shadow:
        0 45px 45px rgba(99,102,241,0.35),
        inset 0 1px 0 rgba(255,255,255,0.6);
}
.header {
    margin-top: 20px;
    margin-bottom: 20px;
    padding: 22px 28px;
}
.header {
    margin-top: 20px;
    padding: 20px 32px;
    border-radius: 28px;
}

/* ===============================
KPI CARD
=============================== */
[data-testid="metric-container"] {
    background: linear-gradient(180deg, #6365e8, #8498ff,#97a8ff, #7dd3fc);
    border-radius: 22px;
    padding: 22px;
    box-shadow:
        0 12px 30px rgba(99,102,241,0.25);
    backdrop-filter: blur(50px);
    text-align: center;
}
[data-testid="metric-container"] label {
    font-size: 18px;
    color: #2f4768;
}
[data-testid="metric-container"] div {
    font-size: 30px;
    font-weight: 700;
    color: #15264d;
}

/* ===============================
FILTER (SELECTBOX)
=============================== */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.6) !important;
    border-radius: 18px !important;
    border: none !important;
    box-shadow:
        0 8px 22px rgba(99,102,241,0.25);
    backdrop-filter: blur(12px);
}
div[data-baseweb="select"] span {
    color: #1e293b !important;
    font-weight: 500;
}

/* ===============================
CHART CONTAINER
=============================== */
.stPlotlyChart {
    background: rgba(255,255,255,0.55);
    border-radius: 26px;
    padding: 22px;
    box-shadow:
        0 18px 40px rgba(99,102,241,0.28);
    backdrop-filter: blur(14px);
    margin-bottom: 35px;
}

/* ===============================
TABLE
=============================== */
.stDataFrame {
    background: rgba(255,255,255,0.6);
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(99,102,241,0.25);
}

/* ===============================
BUTTON
=============================== */
.stButton > button {
    background: linear-gradient(90deg, #818cf8, #7dd3fc);
    color: #0f172a;
    border-radius: 20px;
    font-weight: 600;
    padding: 10px 22px;
    box-shadow: 0 10px 25px rgba(99,102,241,0.35);
}
.stButton > button:hover {
    transform: translateY(-2px);
}

/* ===============================
INPUT & TEXTAREA
=============================== */
.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background: rgba(255,255,255,0.6);
    border-radius: 16px;
    border: none;
}
.kpi-animated {
    background: linear-gradient(200deg,#f6d5ff,#97a8ff, #7dd3fc);
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 50px 65px rgba(99,102,241,0.28);
    backdrop-filter: blur(14px);
    border: 1.5px solid rgba(255, 255, 255, 0.55);
}
.kpi-label {
    border-radius: 20px;
    font-size: 18px;
    color: #1e293b;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 30px;
    font-weight: 700;
    color: #1e293b;
}    
section[data-testid="stSidebar"] .stSelectbox {
    margin-top: 10px;
}
            
/* ===============================
DASHBOARD SPACING FIX
=============================== */
/* MAIN CONTENT WIDTH */
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
}
/* HEADER SPACING */
.header {
    margin-bottom: 25px !important;
}
/* FILTER ROW */
div[data-testid="stHorizontalBlock"]:has(select) {
    margin-bottom: 40px !important;
}
/* FILTER SELECTBOX SPACING */
section[data-testid="stSidebar"] + div select,
.stSelectbox {
    margin-bottom: 5px;
}
/* KPI ROW SPACING */
div[data-testid="stHorizontalBlock"]:has(.kpi-animated) {
    margin-bottom: 15px !important;
}
/* KPI CARD SIZE CONSISTENCY */
.kpi-animated {
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
/* CHART CONTAINER SPACING */
.stPlotlyChart {
    margin-top: 10px !important;
    margin-bottom: 50px !important;
}
/* CHART TITLE SPACING */
.stPlotlyChart h2 {
    margin-bottom: 18px !important;
}
/* DATAFRAME SPACING */
.stDataFrame {
    margin-top: 20px !important;
}
/* GLOBAL SECTION GAP */
section.main > div {
    gap: 28px;
}
/* INSIGHT MESSAGE SPACING */
.stAlert {
    margin-top: 5px;
    margin-bottom: 10px;
}
/* SIDEBAR ACCORDION */
section[data-testid="stSidebar"] .stExpander {
    background: rgba(255,255,255,0.15);
    border-radius: 16px;
    margin-bottom: 12px;
}
section[data-testid="stSidebar"] .stExpander > details {
    padding: 6px 12px;
}
section[data-testid="stSidebar"] button {
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    padding: 10px 8px;
    border-radius: 10px;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.18);
}
/* STICKY FILTER */
.sticky-filter {
    position: sticky;
    top: 15px;
    z-index: 99;
    padding: 18px 20px;
    margin-bottom: 40px;
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);
    border-radius: 26px;
    box-shadow: 0 18px 40px rgba(99,102,241,0.25);
}
/* FADE ANIMATION */
.fade-in {
    animation: fadeUp 0.8s ease-in-out both;
}
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===============================
ACTIVE SIDEBAR
=============================== */       
section[data-testid="stSidebar"] button[aria-selected="true"] {
    background: rgba(255,255,255,0.18) !important; 
    backdrop-filter: blur(8px);

    color: #ffffff !important;
    font-weight: 700;

    box-shadow:
        inset 4px 0 0 rgba(255,255,255,0.5),
        0 8px 22px rgba(0,0,0,0.15);

    opacity: 1 !important;
}

        
/* ===============================
PAGE TRANSITION
=============================== */
.page-transition {
    animation: pageFade .6s ease-in-out both;
}

@keyframes pageFade {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ===============================
SKELETON LOADING KPI
=============================== */
.kpi-skeleton {
    height: 70px;
    border-radius: 16px;
    background: linear-gradient(
        90deg,
        #e5e7eb 30%,
        #f3f4f6 40%,
        #e5e7eb 50%
    );
    background-size: 200%;
    animation: shimmer 1.2s infinite;
}
@keyframes shimmer {
    to {
        background-position-x: -200%;
    }
}

/* ===============================
MOBILE FIX
=============================== */
@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem !important;
    }
    .header {
        font-size: 24px;
    }
}

/* ======================================
SIDEBAR UX 
====================================== */
/* DEFAULT SIDEBAR BUTTON */
section[data-testid="stSidebar"] button {
    color: #e8f8ff !important;
    background: transparent !important;
    border-radius: 14px;
    margin: 6px 0;
    padding: 10px 12px;
    transition: all 0.25s ease;
}
/* HOVER STATE */
section[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.18) !important;
    transform: translateX(4px);
}
/* ACTIVE / SELECTED STATE */
section[data-testid="stSidebar"] button[aria-selected="true"] {
    background: rgba(255,255,255,0.22) !important;   
    backdrop-filter: blur(10px);
    
    color: #ffffff !important;
    font-weight: 700;

    box-shadow:
        inset 4px 0 0 rgba(255,255,255,0.9),
        0 10px 28px rgba(0,0,0,0.18);
    transform: translateX(6px);
}
/* ICON ACTIVE */
section[data-testid="stSidebar"] button[aria-selected="true"] svg {
    fill: #ffffff !important;
}
/* ICON HOVER */
section[data-testid="stSidebar"] button:hover svg {
    fill: #ffffff !important;
}
/* REMOVE FOCUS OUTLINE (CLEAN LOOK) */
section[data-testid="stSidebar"] button:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* ===============================
HOME COMPACT MODE
=============================== */
.home-compact .block-container {
    padding-top: 1.4rem !important;
    padding-bottom: 1.2rem !important;
}
/* KPI lebih ramping */
.home-compact .kpi-animated {
    min-height: 72px;
    padding: 14px;
}
.home-compact .kpi-value {
    font-size: 26px;
}
.home-compact .kpi-label {
    font-size: 14px;
}
/* Chart container lebih pendek */
.home-compact .stPlotlyChart {
    padding: 14px;
    border-radius: 22px;
    margin-bottom: 14px !important;
}
/* Header lebih tipis */
.home-compact .header {
    font-size: 30px;
    padding: 16px 22px;
    margin-bottom: 14px !important;
}
/* Jarak antar row dipersempit */
.home-compact section.main > div {
    gap: 16px;
}

/* =========================
HAPUS SCROLLBAR PLOTLY
========================= */
/* Wrapper plotly */
.stPlotlyChart > div {
    overflow: visible !important;
}
/* SVG chart */
.stPlotlyChart svg {
    overflow: visible !important;
}
/* Container utama chart */
.js-plotly-plot,
.plotly,
.plot-container {
    overflow: visible !important;
}
/* Hilangkan scrollbar internal */
.js-plotly-plot::-webkit-scrollbar {
    display: none !important;
}
/* Firefox */
.js-plotly-plot {
    scrollbar-width: none !important;
}

/* =========================
ANTI CARD KE POTONG
========================= */
.element-container {
    overflow: visible !important;
}
/* Tambah ruang aman bawah */
.block-container {
    padding-bottom: 3rem;
}
/* =========================
HOME COMPACT MODE
========================= */
.home-compact {
    max-height: 100vh;
    overflow: hidden;
}
/* KPI COMPACT */
.home-compact .kpi-animated {
    padding: 12px !important;
    min-height: 80px !important;
}
.home-compact .kpi-label {
    font-size: 14px !important;
}
.home-compact .kpi-value {
    font-size: 22px !important;
}
/* CHART COMPACT */
.home-compact .stPlotlyChart {
    padding: 12px !important;
    margin-bottom: 12px !important;
    border-radius: 18px !important;
}
/* REMOVE EXTRA SPACE */
.home-compact h2 {
    margin-bottom: 8px !important;
}
/* PLOTLY TITLE */
.home-compact .plotly-title {
    margin-bottom: 0px !important;
}
/* COLUMN GAP */
.home-compact section.main > div {
    gap: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# ============ LOAD DATA ============ #
@st.cache_data
def load_data():
    df = pd.read_csv("Sales.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df.dropna(subset=["Date"])

df = load_data()

# ============ SIDEBAR STATE ============ #
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ============ SIDEBAR ============ #
st.markdown("""
<style>
/* Hilangkan padding atas & bawah sidebar */
section[data-testid="stSidebar"] {
    padding-top: 0.0rem;
    padding-bottom: 0.0rem;
}

/* Hilangkan header kosong bawaan Streamlit */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0;
}

/* Konten sidebar rapat */
section[data-testid="stSidebar"] .block-container {
    padding-top: 0.0rem;
    padding-bottom: 0.0rem;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    col = st.columns([1, 6, 1])[1]
    with col:
        logo = Image.open("assets/velocia_logo.png")
        st.image(logo, width=130)

    st.markdown("---")

    with st.expander("🏠 Home", expanded=True):
        if st.button("Overview Home"):
            st.session_state.page = "Home"

    with st.expander("📊 Dashboard", expanded=True):
        if st.button("Detailed"):
            st.session_state.page = "Dashboard"

    with st.expander("📄 Data"):
        if st.button("Document"):
            st.session_state.page = "Document"
        if st.button("Calendar"):
            st.session_state.page = "Calendar"

    with st.expander("💬 Communication"):
        if st.button("Message Center"):
            st.session_state.page = "Message"
        if st.button("Notification"):
            st.session_state.page = "Notification"

    with st.expander("⭐ Feedback"):
        if st.button("Review"):
            st.session_state.page = "Review"

    with st.expander("ℹ️ Info"):
        if st.button("About"):
            st.session_state.page = "About"
        if st.button("Help"):
            st.session_state.page = "Help"

    if st.button("⚙️ Settings"):
        st.session_state.page = "Settings"

# ============ KPI ANIMATION (FIXED) ============ #
def animated_kpi(label, value, prefix="", suffix="", highlight=None, tooltip=None):

    formatted = format_number(value)
    raw_value = f"{value:,.0f}"

    highlight_color = {
        "winner": "#4f46e5",   
        "loser": "#ef4444",    
        None: "#1e293b"
    }.get(highlight)

    badge = {
        "winner": "🏆",
        "loser": "⚠️",
        None: ""
    }.get(highlight)

    tooltip_text = tooltip if tooltip else raw_value

    st.markdown(f"""
    <div class="kpi-animated fade-in" title="{tooltip_text}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{highlight_color}">
            {badge} {prefix}{formatted}{suffix}
        </div>
    </div>
    """, unsafe_allow_html=True)

def format_number(value):
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:,.0f}"

# ============ HOME PAGE ============ #
def detect_column(df, keywords):
    for col in df.columns:
        for key in keywords:
            if key.lower() in col.lower():
                return col
    return None


st.markdown("""
<style>
.home-compact {
    transform: scale(0.83);
    transform-origin: top center;
}

.chart-card {
    background: linear-gradient(
        180deg,
        rgba(255,255,255,0.55),
        rgba(240,245,255,0.75)
    );
    border-radius: 20px;
    padding: 12px 14px 10px 14px;
    box-shadow: 0 10px 26px rgba(90,100,160,0.22);
    overflow: hidden;
}

.card-title {
    font-size: 12px;
    font-weight: 900;
    margin-bottom: 2px;
}

.home-compact .js-plotly-plot text {
    font-size: 9px !important;
}

.home-compact .plotly .legend text {
    font-size: 8.5px !important;
}

.home-compact .plotly .xtick text,
.home-compact .plotly .ytick text {
    font-size: 8.5px !important;
}

.element-container {
    margin-bottom: 0 !important;
}
</style>
""", unsafe_allow_html=True)


def card_open(title):
    st.markdown(f"""
        <div class="chart-card">
            <div class="card-title">{title}</div>
    """, unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def home_page(df):
    st.markdown('<div class="home-compact">', unsafe_allow_html=True)

    revenue_col = detect_column(df, ["revenue", "sales"])
    profit_col = detect_column(df, ["profit"])

    total_revenue = df[revenue_col].sum()
    total_profit = df[profit_col].sum()
    total_orders = len(df)
    aov = total_revenue / total_orders if total_orders else 0
    total_country = df["Country"].nunique()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: animated_kpi("💰 Revenue", total_revenue, "$")
    with k2: animated_kpi("📈 Profit", total_profit, "$")
    with k3: animated_kpi("📦 Orders", total_orders)
    with k4: animated_kpi("🧾 AOV", aov, "$")
    with k5: animated_kpi("🌍 Countries", total_country)

    c1, c2 = st.columns(2)

    with c1:
        card_open("Revenue Trend")
        trend = df.groupby(df["Date"].dt.to_period("M"))[revenue_col].sum().reset_index()
        trend["Date"] = trend["Date"].astype(str)

        fig = px.line(trend, x="Date", y=revenue_col)
        fig.update_layout(
            height=160,
            margin=dict(l=32, r=60, t=10, b=78),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        card_close()

    with c2:
        card_open("Revenue vs Profit")
        fig = px.scatter(
            df,
            x=revenue_col,
            y=profit_col,
            color="Country",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(
            height=160,
            margin=dict(l=12, r=26, t=10, b=70),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        card_close()

    b1, b2, b3 = st.columns(3)

    with b1:
        card_open("Revenue by Age Group")
        age_df = df.groupby("Age_Group")[revenue_col].sum().reset_index()
        fig = px.bar(age_df, x="Age_Group", y=revenue_col)
        fig.update_layout(
            height=155,
            margin=dict(l=82, r=90, t=25, b=88),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        card_close()

    with b2:
        card_open("Revenue by Category")
        cat_df = df.groupby("Product_Category")[revenue_col].sum().reset_index()
        fig = px.pie(
            cat_df,
            names="Product_Category",
            values=revenue_col,
            hole=0.48,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(
            height=155,
            margin=dict(l=10, r=150, t=0.9, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True
        )
        fig.update_traces(textfont_size=9)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        card_close()

    with b3:
        card_open("Sales Map Europe")
        map_df = df.groupby("Country")[revenue_col].sum().reset_index()
        fig = px.choropleth(
            map_df,
            locations="Country",
            locationmode="country names",
            color=revenue_col,
            scope="europe",
            color_continuous_scale=["#bfdbfe", "#6366f1", "#1e3a8a"]
        )
        fig.update_layout(
            height=155,
            margin=dict(l=8, r=8, t=0, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(
                title_font=dict(size=9),
                tickfont=dict(size=8)
            )
        )
        fig.update_geos(
            bgcolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=False
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        card_close()

    st.markdown("</div>", unsafe_allow_html=True)


# ============ DASHBOARD PAGE ============ #
def dashboard_page(df):
    compare_mode = False
    winner = None
    loser = None
    delta_value = 0
    delta_text = None
    revenue_col = detect_column(df, ["revenue", "sales", "amount"])
    profit_col = detect_column(df, ["profit"])
    quantity_col = detect_column(df, ["quantity", "order"])

# ============ HEADER ============ #
    st.markdown(
        '<div class="header">🚴 Bike Sales in Europe</div>',
        unsafe_allow_html=True
    )
# ============ COMPARISON MODE ============ #
    compare_mode = st.toggle("Comparison Mode", value=False)

# ============ FILTER OPTIONS ============ #
    countries = sorted(df["Country"].dropna().unique())
    products = sorted(df["Product"].dropna().unique())
    years = sorted(df["Date"].dt.year.dropna().unique())
    c1, c2, c3 = st.columns(3)
    with c1:
        country = (
            st.multiselect("Country", countries, default=countries[:2])
            if compare_mode else
            st.selectbox("Country", ["All"] + countries)
        )
    with c2:
        product = (
            st.multiselect("Product", products, default=products[:1])
            if compare_mode else
            st.selectbox("Product", ["All"] + products)
        )
    with c3:
        year = (
            st.multiselect("Year", years, default=[years[-1]])
            if compare_mode else
            st.selectbox("Year", ["All"] + years)
        )
# ============ FILTER OPTIONS ============ #
    filtered = df.copy()

    if isinstance(country, list):
        filtered = filtered[filtered["Country"].isin(country)]
    elif country != "All":
        filtered = filtered[filtered["Country"] == country]

    if isinstance(product, list):
        filtered = filtered[filtered["Product"].isin(product)]
    elif product != "All":
        filtered = filtered[filtered["Product"] == product]

    if isinstance(year, list):
        filtered = filtered[filtered["Date"].dt.year.isin(year)]
    elif year != "All":
        filtered = filtered[filtered["Date"].dt.year == year]

# ============ CLEAN NUMERIC ============ #
    for col in [revenue_col, profit_col]:
        if col:
            filtered[col] = pd.to_numeric(
                filtered[col].astype(str)
                .str.replace(",", "")
                .str.replace("$", "")
                .str.replace("€", ""),
                errors="coerce"
            )

    filtered = filtered.dropna(subset=[revenue_col, profit_col])

# ============ KPI CALCULATION ============ #
    total_revenue = filtered[revenue_col].sum()
    total_profit = filtered[profit_col].sum()
    total_orders = len(filtered)
    aov = total_revenue / total_orders if total_orders > 0 else 0

# ============ WINNER / LOSER LOGIC ============ #
    if compare_mode and len(filtered["Country"].unique()) >= 2:
        country_rev = (
            filtered
            .groupby("Country")[revenue_col]
            .sum()
            .sort_values(ascending=False)
        )
        winner = country_rev.index[0]
        loser = country_rev.index[-1]
        top_val = country_rev.iloc[0]
        loser_val = country_rev.iloc[-1]
        if loser_val > 0:
            delta_value = ((top_val - loser_val) / loser_val) * 100
            delta_text = f"{winner} outperform {loser} by {delta_value:.1f}%"


# ============ KPI DISPLAY ============ #
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        animated_kpi(
            "💰 Total Revenue",
            total_revenue,
            "$",
            highlight="winner" if compare_mode and winner else None,
            tooltip=f"Exact: ${total_revenue:,.0f}"
        )
    with k2:
        animated_kpi(
            "📈 Total Profit",
            total_profit,
            "$",
            tooltip=f"Exact: ${total_profit:,.0f}"
        )
    with k3:
        animated_kpi(
            "📦 Orders",
            total_orders,
            tooltip=f"Total Orders: {total_orders:,}"
        )
    with k4:
        animated_kpi(
            "🧾 AOV",
            aov,
            "$",
            tooltip=f"Exact AOV: ${aov:,.2f}"
        )
    if compare_mode and delta_text:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(90deg, #8498ff,#97a8ff, #7dd3fc);
                padding: 14px 14px;
                border-radius: 14px;
                margin-bottom: 18px;
                font-weight: 600;
                color: #1e293b;
                margin-top: 5px;
                box-shadow: 0 8px 25px rgba(99,102,241,0.25);
            ">
                📊 {delta_text}
            </div>
            """,
            unsafe_allow_html=True
        )
        
# ============ EXECUTIVE SUMMARY ============ #
    if compare_mode and winner:
        st.markdown(
            f"""
            <div class="sticky-filter fade-in">
                <b>Executive Summary</b><br>
                During the selected period, <b>{winner}</b> emerges as the
                top-performing country in bike sales across Europe.
                Revenue exceeds <b>{loser}</b> by
                <b>{delta_value:.1f}%</b>, highlighting strong competitive advantage.
            </div>
            """,
            unsafe_allow_html=True
        )

# ============ EXECUTIVE SUMMARY ============ #
    if compare_mode and delta_text:
        st.info(
            f"📊 **Performance Insight**\n\n"
            f"- {delta_text}\n"
            f"- {winner} contributes the highest revenue share.\n"
            f"- Strategic focus on {winner} may maximize profitability."
        )

# ============ CHARTS ============ #
    # Revenue Trend (Time Series)
    trend = (
        filtered
        .groupby([filtered["Date"].dt.to_period("M"), "Country"])[revenue_col]
        .sum()
        .reset_index()
    )
    trend["Date"] = trend["Date"].astype(str)
    fig = px.line(
        trend,
        x="Date",
        y=revenue_col,
        color="Country",
        title="Revenue Trend (Comparison)" if compare_mode else "Revenue Trend"
    )
    fig.update_layout(
        height=360,   
        margin=dict(
            l=80,
            r=80,
            t=20,
            b=140
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=12)
        )
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            y=-0.28,
            x=0.5,
            xanchor="center"
        ),
        height=340
    )
    fig.update_xaxes(
        showgrid=False,
        fixedrange=True 
    )
    fig.update_yaxes(
        showgrid=True,
        fixedrange=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # ============ NEW VISUALIZATIONS ============ #
    v1, v2 = st.columns(2)
    # Bar Chart – Revenue by Age Group
    with v1:
        age_df = (
            filtered
            .groupby("Age_Group")[revenue_col]
            .sum()
            .reset_index()
            .sort_values(revenue_col, ascending=False)
        )
        fig_bar = px.bar(
            age_df,
            x="Age_Group",
            y=revenue_col,
            text_auto=".2s",
            title="Revenue by Age Group"
        )
        fig_bar.update_layout(
            height=330,
            margin=dict(l=20, r=60, t=30, b=120),  
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=20),
        )
        fig_bar.update_traces(
            textposition="inside",
            textfont=dict(size=14, color="white"),
            cliponaxis=True 
        )
        fig_bar.update_xaxes(
            tickangle=-25,
            automargin=True, 
            fixedrange=True
        )
        fig_bar.update_yaxes(
            automargin=True,
            fixedrange=True
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    # Pie Chart – Revenue by Product Category
    with v2:
        category_df = (
            filtered
            .groupby("Product_Category")[revenue_col]
            .sum()
            .reset_index()
        )
        fig_pie = px.pie(
            category_df,
            names="Product_Category",
            values=revenue_col,
            hole=0.45,
            title="Revenue by Product Category",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_pie.update_layout(
            height=330,
            margin=dict(l=40, r=100, t=30, b=110),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_font=dict(size=20),
            legend=dict(
                orientation="h",
                y=-0.25,         
                x=0.5,
                xanchor="center",
                font=dict(size=13)
            )
        )
        fig_pie.update_traces(
            textinfo="percent",
            textposition="inside",
            hole=0.45
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Revenue vs Profit (Scatter)
    fig = px.scatter(
        filtered,
        x=revenue_col,
        y=profit_col,
        color="Country",
        title="Revenue vs Profit",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(
        height=370,
        margin=dict(l=70, r=140, t=70, b=80),  # ⬅ ruang legend
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(
            text="Revenue vs Profit",
            x=0.02,
            y=0.9,
            xanchor="left",
            font=dict(size=22)
        ),
        legend=dict(
            title="Country",
            orientation="v",
            x=0.98,              
            y=0.5,
            xanchor="left",
            yanchor="middle",
            font=dict(size=13),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    # Axis & grid 
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(120,120,140,0.25)",
        zeroline=False,
        linecolor="rgba(120,120,140,0.6)",
        tickfont=dict(color="#555"),
        fixedrange=True
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(120,120,140,0.25)",
        zeroline=False,
        linecolor="rgba(120,120,140,0.6)",
        tickfont=dict(color="#555"),
        fixedrange=True
    )
    # Marker
    fig.update_traces(
        marker=dict(
            size=10,
            opacity=0.85,
            line=dict(width=1, color="rgba(0,0,0,0.35)")
        )
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    # Sales Map Europe
    map_df = (
        filtered
        .groupby("Country")[revenue_col]
        .sum()
        .reset_index()
    )
    fig = px.choropleth(
        map_df,
        locations="Country",
        locationmode="country names",
        color=revenue_col,
        title="Sales Map Europe",
        color_continuous_scale=[
            "#e0f2fe",
            "#38bdf8",
            "#1e3a8a"
        ]
    )
    fig.update_layout(
        height=420,
        margin=dict(l=60, r=30, t=50, b=25),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        geo=dict(
            scope="europe",
            projection_type="natural earth",
            fitbounds="locations",

            bgcolor="rgba(0,0,0,0)",

            showframe=False,         
            showcoastlines=False,
            showcountries=True,
            countrycolor="rgba(30,41,59,0.35)",

            showland=True,
            landcolor="rgba(203,213,225,0.35)",

            lataxis=dict(showgrid=False),
            lonaxis=dict(showgrid=False)
        ),

        coloraxis_colorbar=dict(
            title="Revenue",
            thickness=12,
            len=0.55,
            y=0.5,
            outlinewidth=0       
        ),

        title=dict(
            text="Sales Map Europe",
            x=0.02,
            y=0.95,
            xanchor="left",
            yanchor="top",
            font=dict(size=22)
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# ============ TOP PRODUCT ============ #
    top_product = "N/A"

    if "Product" in filtered.columns and revenue_col:
        prod_rev = (
            filtered
            .groupby("Product")[revenue_col]
            .sum()
            .sort_values(ascending=False)
        )

        if not prod_rev.empty:
            top_product = prod_rev.index[0]

# ============ INSIGHT CALCULATION ============ #
    # Top Country
    top_country = winner if winner else "N/A"
    # Top Age Group
    top_age = "N/A"
    top_age_val = 0
    if not age_df.empty:
        top_age = age_df.iloc[0]["Age_Group"]
        top_age_val = age_df.iloc[0][revenue_col]
    # Top Product Category
    top_category = "N/A"
    top_category_val = 0
    if not category_df.empty:
        top_category = (
            category_df
            .sort_values(revenue_col, ascending=False)
            .iloc[0]["Product_Category"]
        )
        top_category_val = (
            category_df
            .sort_values(revenue_col, ascending=False)
            .iloc[0][revenue_col]
        )
    # Trend Insight
    trend_msg = "Revenue remains relatively stable over time."
    if len(trend["Date"].unique()) > 3:
        trend_msg = (
            "Revenue exhibits noticeable monthly fluctuations, "
            "indicating the presence of seasonal demand patterns."
        )
# ============ EXECUTIVE INSIGHT ============ #
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg,#97a8ff, #7dd3fc);
            border-left: 6px solid #4f46e5;
            padding: 22px 26px;
            border-radius: 18px;
            margin-top: 28px;
            margin-bottom: 28px;
            box-shadow: 0 12px 32px rgba(79,70,229,0.25);
        ">
            <b style="font-size:17px; color:#1e293b;">
                📌 Insights
            </b>
            <ul style="margin-top:14px; line-height:1.9; color:#334155;">
                <li>
                    <b>{top_country}</b> emerges as the leading revenue contributor
                    based on country-level performance comparison.
                </li>
                <li>
                    The <b>{top_age}</b> age group generates the highest revenue,
                    contributing <b>${top_age_val:,.0f}</b> in total sales.
                </li>
                <li>
                    <b>{top_category}</b> dominates product sales,
                    delivering <b>${top_category_val:,.0f}</b> in revenue.
                </li>
                <li>
                    {trend_msg}
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
# ============ OTHER PAGES  ============ #
def document_page(df):
    st.title("📄 Dataset Document")
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇ Download CSV", df.to_csv(index=False), "sales_export.csv")

def calendar_page(df):
    st.title("📅 Sales Calendar")
    start, end = st.date_input("Date Range", [df["Date"].min(), df["Date"].max()])
    f = df[(df["Date"] >= pd.to_datetime(start)) & (df["Date"] <= pd.to_datetime(end))]
    st.metric("Total Revenue", f"${f['Revenue'].sum():,.0f}")
    st.dataframe(f)

def message_page():
    st.title("💬 Message Center")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form("msg"):
        n = st.text_input("Name")
        e = st.text_input("Email")
        c = st.selectbox("Category", ["General", "Support", "Feedback"])
        m = st.text_area("Message")
        if st.form_submit_button("Send"):
            st.session_state.messages.append({"Name": n, "Email": e, "Category": c, "Message": m, "Time": datetime.now()})
            st.success("Message sent!")

    st.dataframe(pd.DataFrame(st.session_state.messages))

def notification_page(df):
    st.title("🔔 Notifications")
    st.info("🔄 System running normally.")

def review_page():
    st.title("⭐ Review")
    r = st.slider("Rate", 1, 5, 5)
    if st.button("Submit"):
        st.success(f"Thanks for rating {r} ⭐")

def about_page():
    st.title("ℹ️ About")
    st.write("Bike Sales in Europe Dashboard using Streamlit & Plotly")

def help_page():
    st.title("❓ Help")
    st.write("Use sidebar navigation to explore features.")

def settings_page():
    st.title("⚙️ Settings")
    if st.button("Reset App"):
        st.experimental_rerun()
# ============ ROUTER ============ #
page = st.session_state.page
{
    "Home": lambda: home_page(df),
    "Dashboard": lambda: dashboard_page(df),
    "Document": lambda: document_page(df),
    "Calendar": lambda: calendar_page(df),
    "Message": message_page,
    "Notification": lambda: notification_page(df),
    "Review": review_page,
    "About": about_page,
    "Help": help_page,
    "Settings": settings_page
}.get(page, lambda: dashboard_page(df))()