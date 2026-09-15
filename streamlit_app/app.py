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
    background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('data:image/jpeg;base64,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ta3qq+xrWta3jWta1rem/gt/jW/h941v+QJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAkP/aAAgBAwEBPwFIP//EABQRAQAAAAAAAAAAAAAAAAAAAJD/2gAIAQIBAT8BSD//xAAUEAEAAAAAAAAAAAAAAAAAAACw/9oACAEBAAY/AkWP/8QAHRABAQEBAAIDAQAAAAAAAAAAAAERECAwQFBggP/aAAgBAQABPyHynhERERERE9QAiIlSpWta3utaqqqqq+gBVVVVVXxvuiIiIiIiInpAJUqVKlSta1rWta1rVq1aq9L5gVVVVVVVeX3xE7ERERETxCVKlSpUqVrWta1rWta1rVq1atWrfQAqqqqqqqqvunJyIiIiIiJ4CVKpKlSpUqVrWt43jeNa1q1atWrVKW9Kqqqqqqqqqr74idiIiIiInESpUqVKlSp7wABatWrVq1atW9Kqqqqqqqqq+2InhERERERESpUqVKlSpUqVvmBvoAWrVq1atWrVKqqqqqqvaq++ciIiIiIiIiJUqVKlSpUqVrWta1rWt41rVKatWrVq1atWqqqqqqqqqq/AidiIiIiIiJUqVKlSpUrWta1rW8b01rWtWrVq1atWrVqqqqqqqqqqvviInIiIiIiIiVKlSpUqVK1rWta1rWta1rWtWrVq1atWrVqqqqqqqqqqvvicnYnYiIiclSpUqVrWta1rWta1rWta1rVq1atWrVqqqqqqqqvKq+6InYnIiIiIiIlSpUqVK1rWta1rWta1rWta1a1atWrVqqqqqqqqqqvwpyciIiIiIiclSpUrWta1rWta1rWta1rWrVq1atWrVVVVVVVVVX4c8IiIidiJeytala1rWta1rWta1rWtWtatWrVq1avKqqqqqr8aIiIicnYlSpWta1K1rWta1rWta1rWta1rVq1atVVVVVVVVX48RERE5PDUvNa1rWta1rWta1rWta1rWrVq1avKqqqqvL8meETk8N5Kla1rWta1rWta1rWta1rWta1vN5VVVVV+gnnLzWta1rWta1rWta1rWta1rWtb4VeX6zWta1rWta1rWta1rWta1rWt+21rWta1rWta1rWta1rWta1rW/Z61rWta1rWta1rWta1rWta1v2uta1rWta1rWta1rWta1rW/da1rWta1rWta3mta1rfvNa1rWta1rWta1rfweta1vhrW/xjjOYxjGM5jPwuMYxnhjPw+MYxjGflbyr95PgX7/Wta1rWta1rWta38BrWta1rWta1rW/gta1rWta1rWt/Ea1rW/zD/9oADAMBAAIAAwAAABAb7YppLK9WfZwTV1WZEGvMWH5HUHwwpt2nI5J6JYIo4qap75s3FahnGmNF89LgbP3ZXFFiC9GlLa6boL76LJpKIpNn1JyX9tnv/X+PMvuEqNnyaNWdLJ6o546L666bzuMNUYbzt/xndtvPcsmV8sVy4FUtL5po7o5qZKrozPNNETpJwl8NHn3X1H1vvFSL42Ff7JpoJbKp65Zo7esOU0wLqyEXFu8tN+lHUI4JDUFNfpp7Kr66rL5ps9tOt3SiwZrnEXHEHEDZbbSw3v8Aj3eaOOWCWiKKyenXffbtkkCCy3LzyjTyygg8ppbrrrmay2KCWC++uOfHrzbj/DwUAgUXfXiCuyT/AB220687jjgqvnlughhhr/2y91wwx006xrAGZTx02z22y88okkrlvvuhvsstjm86wy5fQ2nhvvjppkroywzzz3vssjklvtqnhusrrsp274iqlkmDDLHKBIKhunoghjjsrlivvnoqmpshmsrnpqnvvvLBDPcNPKBvljnusqntkqqlvuhrqulpshgssortqjCABXqhLFIEsgijnpkiqrrgvgnloqqumrtnnnusnmpsHPKOENGNPnlpmiqqqtligjuvltqqqqqjtvpvkmjhssDKGBIBOJkiqqqrrluvvvnonngqqqqqqnprnggjhlDENDAJNlqpqqqtlitnsvohrultprq7orqpknAMDDOAHHHFHlllhllkvrgsvohuvguul31319g3vvsMMMJDFLPiqqummiuqlnrgghvtqlt66666+/w/vuvvPPDnvvvqvq6q6qt1gvtiwv/EAB8RAAECBwEBAAAAAAAAAAAAABEAARAgMEBBUGBhcP/aAAgBAwEBPxCwM7PE3T1GeJuXmCCCEjXw042QQ4gREG0oQQgEOHFMdifinmm81OJs2GKn/8QAHBEAAgIDAQEAAAAAAAAAAAAAAREAECAwQFBg/9oACAECAQE/EMxpUUUVKKEaDwChoAtURCIszxDAUIKeJhFKzZ2ixYoUDT2mjtGbxeTp+C44448H1inpduz4D73bjjwccccfhOOOPge5x/AHhODp4CDa/aXyLj+NOkeA8hw//8QAIBAB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') no-repeat center center fixed !important; background-size: cover !important;
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
    background: #1d4ed8 !important;
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





