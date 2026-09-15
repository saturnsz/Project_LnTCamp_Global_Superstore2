"""
Page 2: Orders Explorer
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.db import get_orders_table, get_distinct_values

st.set_page_config(page_title="Orders — StoreIQ", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[data-testid="stApp"]{font-family:'Inter',sans-serif!important;background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('data:image/jpeg;base64,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ta3qq+xrWta3jWta1rem/gt/jW/h941v+QJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAkP/aAAgBAwEBPwFIP//EABQRAQAAAAAAAAAAAAAAAAAAAJD/2gAIAQIBAT8BSD//xAAUEAEAAAAAAAAAAAAAAAAAAACw/9oACAEBAAY/AkWP/8QAHRABAQEBAAIDAQAAAAAAAAAAAAERECAwQFBggP/aAAgBAQABPyHynhERERERE9QAiIlSpWta3utaqqqqq+gBVVVVVXxvuiIiIiIiInpAJUqVKlSta1rWta1rVq1aq9L5gVVVVVVVeX3xE7ERERETxCVKlSpUqVrWta1rWta1rVq1atWrfQAqqqqqqqqvunJyIiIiIiJ4CVKpKlSpUqVrWt43jeNa1q1atWrVKW9Kqqqqqqqqqr74idiIiIiInESpUqVKlSp7wABatWrVq1atW9Kqqqqqqqqq+2InhERERERESpUqVKlSpUqVvmBvoAWrVq1atWrVKqqqqqqvaq++ciIiIiIiIiJUqVKlSpUqVrWta1rWt41rVKatWrVq1atWqqqqqqqqqq/AidiIiIiIiJUqVKlSpUrWta1rW8b01rWtWrVq1atWrVqqqqqqqqqqvviInIiIiIiIiVKlSpUqVK1rWta1rWta1rWtWrVq1atWrVqqqqqqqqqqvvicnYnYiIiclSpUqVrWta1rWta1rWta1rVq1atWrVqqqqqqqqvKq+6InYnIiIiIiIlSpUqVK1rWta1rWta1rWta1a1atWrVqqqqqqqqqqvwpyciIiIiIiclSpUrWta1rWta1rWta1rWrVq1atWrVVVVVVVVVX4c8IiIidiJeytala1rWta1rWta1rWtWtatWrVq1avKqqqqqr8aIiIicnYlSpWta1K1rWta1rWta1rWta1rVq1atVVVVVVVVX48RERE5PDUvNa1rWta1rWta1rWta1rWrVq1avKqqqqvL8meETk8N5Kla1rWta1rWta1rWta1rWta1vN5VVVVV+gnnLzWta1rWta1rWta1rWta1rWtb4VeX6zWta1rWta1rWta1rWta1rWt+21rWta1rWta1rWta1rWta1rW/Z61rWta1rWta1rWta1rWta1v2uta1rWta1rWta1rWta1rW/da1rWta1rWta3mta1rfvNa1rWta1rWta1rfweta1vhrW/xjjOYxjGM5jPwuMYxnhjPw+MYxjGflbyr95PgX7/Wta1rWta1rWta38BrWta1rWta1rW/gta1rWta1rWt/Ea1rW/zD/9oADAMBAAIAAwAAABAb7YppLK9WfZwTV1WZEGvMWH5HUHwwpt2nI5J6JYIo4qap75s3FahnGmNF89LgbP3ZXFFiC9GlLa6boL76LJpKIpNn1JyX9tnv/X+PMvuEqNnyaNWdLJ6o546L666bzuMNUYbzt/xndtvPcsmV8sVy4FUtL5po7o5qZKrozPNNETpJwl8NHn3X1H1vvFSL42Ff7JpoJbKp65Zo7esOU0wLqyEXFu8tN+lHUI4JDUFNfpp7Kr66rL5ps9tOt3SiwZrnEXHEHEDZbbSw3v8Aj3eaOOWCWiKKyenXffbtkkCCy3LzyjTyygg8ppbrrrmay2KCWC++uOfHrzbj/DwUAgUXfXiCuyT/AB220687jjgqvnlughhhr/2y91wwx006xrAGZTx02z22y88okkrlvvuhvsstjm86wy5fQ2nhvvjppkroywzzz3vssjklvtqnhusrrsp274iqlkmDDLHKBIKhunoghjjsrlivvnoqmpshmsrnpqnvvvLBDPcNPKBvljnusqntkqqlvuhrqulpshgssortqjCABXqhLFIEsgijnpkiqrrgvgnloqqumrtnnnusnmpsHPKOENGNPnlpmiqqqtligjuvltqqqqqjtvpvkmjhssDKGBIBOJkiqqqrrluvvvnonngqqqqqqnprnggjhlDENDAJNlqpqqqtlitnsvohrultprq7orqpknAMDDOAHHHFHlllhllkvrgsvohuvguul31319g3vvsMMMJDFLPiqqummiuqlnrgghvtqlt66666+/w/vuvvPPDnvvvqvq6q6qt1gvtiwv/EAB8RAAECBwEBAAAAAAAAAAAAABEAARAgMEBBUGBhcP/aAAgBAwEBPxCwM7PE3T1GeJuXmCCCEjXw042QQ4gREG0oQQgEOHFMdifinmm81OJs2GKn/8QAHBEAAgIDAQEAAAAAAAAAAAAAAREAECAwQFBg/9oACAECAQE/EMxpUUUVKKEaDwChoAtURCIszxDAUIKeJhFKzZ2ixYoUDT2mjtGbxeTp+C44448H1inpduz4D73bjjwccccfhOOOPge5x/AHhODp4CDa/aXyLj+NOkeA8hw//8QAIBAB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') no-repeat center center fixed !important; background-size: cover !important;color:#ffffff!important;}
#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:#0a0a0a!important;border-right:1px solid #222222!important;}
[data-testid="metric-container"]{background:#111111!important;border:1px solid #222222!important;padding:1rem 1.2rem!important;}
[data-testid="stMetricValue"]{font-size:1.6rem!important;font-weight:500!important;color:#ffffff!important;}
[data-testid="stMetricLabel"]{color:#888888!important;font-size:0.72rem!important;text-transform:uppercase;letter-spacing:0.05em;}
.page-header{background:#111111;border-left:4px solid #3b82f6;padding:1.5rem 2rem;margin-bottom:1.5rem;}
.page-header h1{margin:0!important;font-size:1.6rem!important;font-weight:400!important;color:#ffffff;}
.page-header p{color:#888888;margin:0.3rem 0 0;font-size:0.9rem;}
.stButton>button{background:#111111!important;color:#ffffff!important;border:1px solid #333333!important;border-radius:0!important;font-weight:400!important;}
.stButton>button p { color: #ffffff !important; }
.stButton>button:hover{border-color:#3b82f6!important;color:#3b82f6!important;}
[data-testid="stSelectbox"] > div, [data-testid="stTextInput"] > div > input, [data-testid="stNumberInput"] > div > input { background: #111111 !important; border: 1px solid #333333 !important; color: #ffffff !important; border-radius: 0 !important; }
hr{border-color:#222222!important;}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:#000000}::-webkit-scrollbar-thumb{background:#333333}
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

st.markdown("""
<div class="page-header">
    <h1>Orders Explorer</h1>
    <p>Browse and filter orders</p>
</div>
""", unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("Filter & Search", expanded=True):
    fc1, fc2, fc3, fc4 = st.columns([2, 1.2, 1.2, 0.8])
    search   = fc1.text_input("Search (Order ID / Customer / Product)", placeholder="Search...")
    categories = ["All"] + get_distinct_values("dim_products", "category")
    markets    = ["All"] + get_distinct_values("dim_locations", "market")
    cat    = fc2.selectbox("Category", categories)
    market = fc3.selectbox("Market",   markets)
    limit  = fc4.select_slider("Max Rows", [100, 250, 500, 1000], value=500)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner="Loading orders…")
def load_orders(search, cat, market, limit):
    return get_orders_table(search=search, category=cat, market=market, limit=limit)

df = load_orders(search, cat, market, limit)

# ── KPI row ───────────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Rows Shown",      f"{len(df):,}")
m2.metric("Total Sales",     f"${df['Sales (USD)'].sum():,.0f}")
m3.metric("Total Profit",    f"${df['Profit (USD)'].sum():,.0f}")
m4.metric("Total Qty",       f"{df['Qty'].sum():,}" if 'Qty' in df.columns else "—")
m5.metric("Avg Discount",    f"{df['Discount (%)'].mean():.1f}%" if 'Discount (%)' in df.columns else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Profit color styling ───────────────────────────────────────────────────────
def color_profit(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return "color: #3b82f6"
        elif val < 0:
            return "color: #888888"
    return ""

styled = df.style.map(color_profit, subset=["Profit (USD)"])

st.dataframe(styled, use_container_width=True, hide_index=True, height=480)

# ── Download ───────────────────────────────────────────────────────────────────
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "orders_export.csv", "text/csv", use_container_width=False)





