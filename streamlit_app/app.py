"""
StoreIQ Admin — Main Entry Point
Minimalist Black, White, and BLUE Theme
"""
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StoreIQ Admin",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS / Design System ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Colors: Black (#000000), White (#ffffff), BLUE (#3b82f6), Dark Grey (#111111) ── */

html, body, [data-testid="stApp"] {
    font-family: 'Inter', sans-serif !important;
    background: #000000 !important;
    color: #ffffff !important;
}

#MainMenu, footer { visibility: hidden; }

[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #222222 !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #888888 !important;
    font-size: 0.8rem;
}

.card {
    background: #111111;
    border: 1px solid #222222;
    padding: 1.5rem;
    transition: all 0.2s;
}
.card:hover {
    border-color: #3b82f6;
}

[data-testid="metric-container"] {
    background: #111111 !important;
    border: 1px solid #222222 !important;
    padding: 1rem 1.2rem !important;
    transition: all 0.2s;
}
[data-testid="metric-container"]:hover { 
    border-color: #3b82f6 !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 500 !important;
    color: #ffffff !important;
}
[data-testid="stMetricLabel"] {
    color: #888888 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricDelta"] svg { display: none; }

.stButton > button {
    background: #3b82f6 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.8 !important;
}

[data-testid="stSelectbox"] > div,
[data-testid="stTextInput"] > div > input,
[data-testid="stNumberInput"] > div > input {
    background: #111111 !important;
    border: 1px solid #333333 !important;
    color: #ffffff !important;
    border-radius: 0 !important;
}

[data-testid="stDataFrame"] {
    border-radius: 0 !important;
}
.dvn-scroller { background: #111111 !important; }

[data-testid="stTabs"] button {
    color: #888888 !important;
    font-weight: 400 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
}

.js-plotly-plot .plotly { border-radius: 0; }
hr { border-color: #222222 !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #000000; }
::-webkit-scrollbar-thumb { background: #333333; }

.page-header {
    background: #111111;
    border-left: 4px solid #3b82f6;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    margin: 0 !important;
    font-size: 1.6rem !important;
    font-weight: 400 !important;
    color: #ffffff;
}
.page-header p { color: #888888; margin: 0.3rem 0 0; font-size: 0.9rem; }

.sidebar-logo {
    font-size: 1.2rem;
    font-weight: 500;
    color: #3b82f6;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.sidebar-version {
    font-size: 0.7rem;
    color: #666666;
}

[data-testid="stSlider"] [data-testid="stSlider"] { color: #3b82f6 !important; }
@media (max-width: 768px) {
    .page-header { padding: 1rem !important; margin-bottom: 1rem !important; }
    .page-header h1 { font-size: 1.3rem !important; }
    .card { padding: 1rem !important; }
    [data-testid="metric-container"] { padding: 0.8rem 1rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    .result-card { padding: 1.2rem !important; }
    .pred-usd { font-size: 2rem !important; }
    .badge-profit, .badge-loss { font-size: 1rem !important; padding: 0.4rem 1rem !important; }
    .input-section { padding: 1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar branding ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">StoreIQ Admin</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-version">Global Superstore Analytics</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <small style='color:#666666'>
        Navigate using the pages above.<br>
        Data: Global Superstore Dataset<br>
        Model: XGBoost
        </small>
        """,
        unsafe_allow_html=True,
    )

# ── Home content ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>StoreIQ Admin Dashboard</h1>
    <p>Minimalist Analytics & Prediction Platform</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3 style='color:#3b82f6;margin:0 0 0.5rem;font-weight:400;font-size:1.1rem'>Dashboard</h3>
        <p style='color:#888888;font-size:0.85rem;margin:0'>KPI Cards, Revenue Trends, Profit by Market, and interactive visualizations.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3 style='color:#3b82f6;margin:0 0 0.5rem;font-weight:400;font-size:1.1rem'>Data Explorer</h3>
        <p style='color:#888888;font-size:0.85rem;margin:0'>Explore Orders, Products, Customers, and Locations with filters.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3 style='color:#3b82f6;margin:0 0 0.5rem;font-weight:400;font-size:1.1rem'>AI Predictor</h3>
        <p style='color:#888888;font-size:0.85rem;margin:0'>Profit/Loss Classification and USD Profit Estimation using XGBoost.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### Overview")

cols = st.columns(4)
stats = [
    ("51,290", "Order Items"),
    ("25,753", "Total Orders"),
    ("4,873", "Customers"),
    ("10,292", "Products"),
]
for col, (val, label) in zip(cols, stats):
    col.markdown(f"""
    <div class="card" style="text-align:center">
        <div style="font-size:1.8rem;font-weight:400;color:#ffffff">{val}</div>
        <div style="color:#888888;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;margin-top:0.5rem">{label}</div>
    </div>
    """, unsafe_allow_html=True)


