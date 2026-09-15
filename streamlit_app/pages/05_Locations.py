"""
Page 5: Locations Explorer
"""
import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.db import get_locations_table, get_distinct_values, get_profit_by_market, get_sales_by_region

st.set_page_config(page_title="Locations — StoreIQ", layout="wide")

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
    <h1>Locations</h1>
    <p>Geographical analysis by Market, Region, Country & City</p>
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
        font=dict(family="Inter", color="#888888", size=11),
        title=dict(text=title, font=dict(color=WHITE, size=13, weight="normal"), x=0.02),
        margin=dict(l=16,r=16,t=40,b=16), height=height,
        xaxis=dict(gridcolor="#1a1a1a", linecolor="#333333"),
        yaxis=dict(gridcolor="#1a1a1a", linecolor="#333333"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("Filter & Search", expanded=True):
    fc1, fc2 = st.columns([2, 1.5])
    search = fc1.text_input("Search City / Country / State", placeholder="Search locations...")
    markets = ["All"] + get_distinct_values("dim_locations", "market")
    market  = fc2.selectbox("Market", markets)

@st.cache_data(ttl=120, show_spinner="Loading locations…")
def load_locations(search, market):
    return get_locations_table(search=search, market=market)

@st.cache_data(ttl=300)
def load_market(): return get_profit_by_market()

@st.cache_data(ttl=300)
def load_region(): return get_sales_by_region()

df      = load_locations(search, market)
df_mkt  = load_market()
df_reg  = load_region()

# ── KPI ───────────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Locations Shown", f"{len(df):,}")
m2.metric("Markets",         f"{df['Market'].nunique()}" if 'Market' in df.columns else "—")
m3.metric("Regions",         f"{df['Region'].nunique()}" if 'Region' in df.columns else "—")
m4.metric("Countries",       f"{df['Country'].nunique()}" if 'Country' in df.columns else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
cc1, cc2 = st.columns(2)

with cc1:
    df_m = df_mkt.sort_values("profit")
    colors = [GREY_D if v < 0 else BLUE for v in df_m["profit"]]
    fig = go.Figure(go.Bar(
        x=df_m["profit"], y=df_m["market"], orientation="h",
        marker_color=colors,
        text=df_m["profit"].apply(lambda v: f"${v:,.0f}"),
        textposition="auto", textfont=dict(color=WHITE, size=10),
    ))
    dark_layout(fig, "Profit by Market", height=320)
    st.plotly_chart(fig, use_container_width=True)

with cc2:
    df_top_region = df_reg.sort_values("sales", ascending=False).head(12)
    fig = go.Figure(go.Bar(
        x=df_top_region["sales"], y=df_top_region["region"],
        orientation="h",
        marker=dict(
            color=df_top_region["profit"],
            colorscale=[[0, GREY_D], [0.5, GREY_L], [1, BLUE]],
            showscale=True,
            colorbar=dict(title="Profit", tickfont=dict(color="#888888"), title_font=dict(color="#888888")),
        ),
        text=df_top_region["sales"].apply(lambda v: f"${v/1e6:.1f}M"),
        textposition="outside", textfont=dict(color="#888888", size=10),
    ))
    dark_layout(fig, "Top Regions by Sales (color=Profit)", height=320)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown(f"#### Location List — `{len(df):,}` records")
st.dataframe(df, use_container_width=True, hide_index=True, height=400)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "locations_export.csv", "text/csv")


