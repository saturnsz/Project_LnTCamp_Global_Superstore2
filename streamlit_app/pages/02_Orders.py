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
html,body,[data-testid="stApp"]{font-family:'Inter',sans-serif!important;background:#000000!important;color:#ffffff!important;}
#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:#0a0a0a!important;border-right:1px solid #222222!important;}
[data-testid="metric-container"]{background:#111111!important;border:1px solid #222222!important;padding:1rem 1.2rem!important;}
[data-testid="stMetricValue"]{font-size:1.6rem!important;font-weight:500!important;color:#ffffff!important;}
[data-testid="stMetricLabel"]{color:#888888!important;font-size:0.72rem!important;text-transform:uppercase;letter-spacing:0.05em;}
.page-header{background:#111111;border-left:4px solid #3b82f6;padding:1.5rem 2rem;margin-bottom:1.5rem;}
.page-header h1{margin:0!important;font-size:1.6rem!important;font-weight:400!important;color:#ffffff;}
.page-header p{color:#888888;margin:0.3rem 0 0;font-size:0.9rem;}
.stButton>button{background:#111111!important;color:#ffffff!important;border:1px solid #333333!important;border-radius:0!important;font-weight:400!important;}
.stButton>button:hover{border-color:#3b82f6!important;color:#3b82f6!important;}
[data-testid="stSelectbox"] > div, [data-testid="stTextInput"] > div > input, [data-testid="stNumberInput"] > div > input { background: #111111 !important; border: 1px solid #333333 !important; color: #ffffff !important; border-radius: 0 !important; }
hr{border-color:#222222!important;}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:#000000}::-webkit-scrollbar-thumb{background:#333333}
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

styled = df.style.applymap(color_profit, subset=["Profit (USD)"])

st.dataframe(styled, use_container_width=True, hide_index=True, height=480)

# ── Download ───────────────────────────────────────────────────────────────────
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "orders_export.csv", "text/csv", use_container_width=False)

