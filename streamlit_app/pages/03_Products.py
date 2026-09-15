"""
Page 3: Products Explorer
"""
import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.db import get_products_table, get_distinct_values, get_sales_by_category, get_top_subcategory

st.set_page_config(page_title="Products — StoreIQ", layout="wide")

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
[data-testid="stSelectbox"] > div, [data-testid="stTextInput"] > div > input { background: #111111 !important; border: 1px solid #333333 !important; color: #ffffff !important; border-radius: 0 !important; }
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
    <h1>Products Explorer</h1>
    <p>Product catalog with category breakdown</p>
</div>
""", unsafe_allow_html=True)

CHART_BG="#000000"
BLUE="#3b82f6"
WHITE="#ffffff"
GREY_L="#aaaaaa"
GREY_D="#444444"

def dark_layout(fig, title="", height=300):
    fig.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
        font=dict(family="Inter",color="#888888",size=11),
        title=dict(text=title,font=dict(color=WHITE,size=13,weight="normal"),x=0.02),
        margin=dict(l=16,r=16,t=40,b=16), height=height,
        xaxis=dict(gridcolor="#1a1a1a",linecolor="#333333"),
        yaxis=dict(gridcolor="#1a1a1a",linecolor="#333333"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("Filter & Search", expanded=True):
    fc1, fc2 = st.columns([2, 1.5])
    search = fc1.text_input("Search Product / Sub-Category", placeholder="Search...")
    categories = ["All"] + get_distinct_values("dim_products", "category")
    cat = fc2.selectbox("Category", categories)

@st.cache_data(ttl=120, show_spinner="Loading products…")
def load_products(search, cat):
    return get_products_table(search=search, category=cat)

df = load_products(search, cat)

# ── Stats row ─────────────────────────────────────────────────────────────────
m1, m2, m3 = st.columns(3)
m1.metric("Total Products", f"{len(df):,}")
if not df.empty:
    m2.metric("Categories", f"{df['Category'].nunique()}")
    m3.metric("Sub-Categories", f"{df['Sub-Category'].nunique()}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts row ───────────────────────────────────────────────────────────────
cc1, cc2 = st.columns(2)

with cc1:
    @st.cache_data(ttl=300)
    def load_cat_sales(): return get_sales_by_category()
    dfc = load_cat_sales()
    fig = go.Figure(go.Pie(
        labels=dfc["category"], values=dfc["sales"], hole=0.6,
        marker=dict(colors=[BLUE, GREY_L, GREY_D]),
        textinfo="label+percent", textfont=dict(size=11,color=WHITE),
    ))
    fig.update_layout(showlegend=False)
    dark_layout(fig, "Sales Share by Category", height=280)
    st.plotly_chart(fig, use_container_width=True)

with cc2:
    @st.cache_data(ttl=300)
    def load_top_sub(): return get_top_subcategory()
    dfs = load_top_sub().sort_values("sales", ascending=True).tail(10)
    colors = [BLUE if i >= len(dfs)-3 else GREY_D for i in range(len(dfs))]
    fig = go.Figure(go.Bar(
        x=dfs["sales"], y=dfs["sub_category"], orientation="h",
        marker_color=colors,
        text=dfs["sales"].apply(lambda v: f"${v/1000:.0f}K"),
        textposition="outside", textfont=dict(color="#888888",size=10),
    ))
    dark_layout(fig, "Top Sub-Categories by Sales", height=280)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown(f"#### Product Catalog — `{len(df):,}` items")
st.dataframe(df, use_container_width=True, hide_index=True, height=420)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "products_export.csv", "text/csv")


