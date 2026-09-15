"""
Page 1: Dashboard — KPI + Charts
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.db import (
    get_kpi, get_revenue_by_year, get_sales_by_category,
    get_profit_by_market, get_top_subcategory, get_orders_by_shipmode,
    get_monthly_trend, get_profit_vs_discount, get_segment_stats,
    get_priority_stats, get_sales_by_region,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard — StoreIQ", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [data-testid="stApp"] { font-family:'Inter',sans-serif!important; background:#000000!important; color:#ffffff!important; }
#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:#0a0a0a!important;border-right:1px solid #222222!important;}
[data-testid="metric-container"]{background:#111111!important;border:1px solid #222222!important;padding:1rem 1.2rem!important;transition:all 0.2s;}
[data-testid="metric-container"]:hover{border-color:#3b82f6!important;}
[data-testid="stMetricValue"]{font-size:1.8rem!important;font-weight:500!important;color:#ffffff!important;}
[data-testid="stMetricLabel"]{color:#888888!important;font-size:0.75rem!important;text-transform:uppercase;letter-spacing:0.05em;}
.page-header{background:#111111;border-left:4px solid #3b82f6;padding:1.5rem 2rem;margin-bottom:1.5rem;}
.page-header h1{margin:0!important;font-size:1.6rem!important;font-weight:400!important;color:#ffffff;}
.page-header p{color:#888888;margin:0.3rem 0 0;font-size:0.9rem;}
hr{border-color:#222222!important;}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:#000000}::-webkit-scrollbar-thumb{background:#333333}
</style>
""", unsafe_allow_html=True)

# ── Minimalist Palette ────────────────────────────────────────────────────────
CHART_BG   = "#000000"
CHART_PAPER = "#000000"
AXIS_COLOR  = "#333333"
TEXT_COLOR  = "#888888"
GRID_COLOR  = "#1a1a1a"
BLUE = "#3b82f6"
WHITE = "#ffffff"
GREY_LIGHT = "#aaaaaa"
GREY_DARK = "#444444"

PALETTE = [BLUE, WHITE, GREY_LIGHT, GREY_DARK, "#666666", "#cccccc", "#bbbbbb"]

def dark_layout(fig, title="", height=360):
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_PAPER,
        font=dict(family="Inter", color=TEXT_COLOR, size=11),
        title=dict(text=title, font=dict(color=WHITE, size=13, family="Inter", weight="normal"), x=0.02),
        margin=dict(l=16, r=16, t=40, b=16),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=AXIS_COLOR, tickcolor=AXIS_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=AXIS_COLOR, tickcolor=AXIS_COLOR),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=300)
def load_all():
    return {
        "kpi":         get_kpi(),
        "rev_year":    get_revenue_by_year(),
        "sales_cat":   get_sales_by_category(),
        "profit_mkt":  get_profit_by_market(),
        "top_sub":     get_top_subcategory(),
        "ship_mode":   get_orders_by_shipmode(),
        "trend":       get_monthly_trend(),
        "pv_disc":     get_profit_vs_discount(),
        "segment":     get_segment_stats(),
        "priority":    get_priority_stats(),
        "region":      get_sales_by_region(),
    }

data = load_all()
kpi  = data["kpi"]

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>Dashboard Overview</h1>
    <p>Global Superstore — Analytics & Business Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Revenue",    f"${kpi['total_revenue']:,.0f}")
k2.metric("Total Orders",     f"{kpi['total_orders']:,}")
k3.metric("Total Profit",     f"${kpi['total_profit']:,.0f}")
k4.metric("Profit Margin",    f"{kpi['profit_margin_pct']:.1f}%")
k5.metric("Total Customers",  f"{kpi['total_customers']:,}")
k6.metric("Avg Discount",     f"{kpi['avg_discount_pct']:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 1
# ═══════════════════════════════════════════════════════════════════════════════
r1c1, r1c2 = st.columns([1, 1.6])

with r1c1:
    df = data["rev_year"]
    fig = go.Figure()
    fig.add_bar(x=df["year"], y=df["revenue"], name="Revenue",
                marker_color=BLUE, marker_line_color="rgba(0,0,0,0)")
    fig.add_bar(x=df["year"], y=df["profit"], name="Profit",
                marker_color=GREY_DARK, marker_line_color="rgba(0,0,0,0)")
    fig.update_layout(barmode="group")
    dark_layout(fig, "Revenue & Profit by Year")
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    df = data["trend"]
    df["period"] = df["year"].astype(str) + "-W" + df["week_num"].astype(str).str.zfill(2)
    df = df.iloc[::2].reset_index(drop=True)
    fig = go.Figure()
    fig.add_scatter(x=df["period"], y=df["sales"], mode="lines",
                    name="Sales", line=dict(color=BLUE, width=1.5),
                    fill="tozeroy", fillcolor="rgba(59,130,246,0.1)")
    fig.add_scatter(x=df["period"], y=df["profit"], mode="lines",
                    name="Profit", line=dict(color=GREY_LIGHT, width=1.5),
                    fill="tozeroy", fillcolor="rgba(255,255,255,0.05)")
    fig.update_xaxes(showticklabels=False)
    dark_layout(fig, "Weekly Sales & Profit Trend", height=360)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 2
# ═══════════════════════════════════════════════════════════════════════════════
r2c1, r2c2, r2c3 = st.columns(3)

with r2c1:
    df = data["sales_cat"]
    fig = go.Figure(go.Pie(
        labels=df["category"], values=df["sales"],
        hole=0.6,
        marker=dict(colors=[BLUE, GREY_LIGHT, GREY_DARK]),
        textinfo="label+percent",
        textfont=dict(size=11, color=WHITE),
    ))
    fig.update_layout(showlegend=False)
    dark_layout(fig, "Sales by Category", height=340)
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    df = data["profit_mkt"].sort_values("profit")
    colors = [GREY_DARK if v < 0 else BLUE for v in df["profit"]]
    fig = go.Figure(go.Bar(
        x=df["profit"], y=df["market"],
        orientation="h",
        marker_color=colors,
        text=df["profit"].apply(lambda v: f"${v:,.0f}"),
        textposition="auto",
        textfont=dict(color=WHITE, size=10),
    ))
    dark_layout(fig, "Profit by Market", height=340)
    st.plotly_chart(fig, use_container_width=True)

with r2c3:
    df = data["ship_mode"]
    fig = go.Figure(go.Pie(
        labels=df["ship_mode"], values=df["order_count"],
        hole=0.6,
        marker=dict(colors=PALETTE),
        textinfo="label+percent",
        textfont=dict(size=11, color=WHITE),
    ))
    fig.update_layout(showlegend=False)
    dark_layout(fig, "Orders by Ship Mode", height=340)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 3
# ═══════════════════════════════════════════════════════════════════════════════
r3c1, r3c2 = st.columns([1.6, 1])

with r3c1:
    df = data["top_sub"].sort_values("sales")
    colors_sub = [BLUE if i >= len(df)-3 else GREY_DARK for i in range(len(df))]
    fig = go.Figure(go.Bar(
        x=df["sales"], y=df["sub_category"],
        orientation="h",
        marker_color=colors_sub,
        text=df["sales"].apply(lambda v: f"${v/1000:.0f}K"),
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=10),
    ))
    dark_layout(fig, "Top 10 Sub-Categories by Sales", height=380)
    st.plotly_chart(fig, use_container_width=True)

with r3c2:
    df = data["segment"]
    fig = go.Figure()
    fig.add_bar(x=df["segment"], y=df["sales"], name="Sales",
                marker_color=BLUE)
    fig.add_bar(x=df["segment"], y=df["profit"], name="Profit",
                marker_color=GREY_DARK)
    fig.update_layout(barmode="group")
    dark_layout(fig, "Sales & Profit by Segment", height=380)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 4
# ═══════════════════════════════════════════════════════════════════════════════
r4c1, r4c2 = st.columns([1.6, 1])

with r4c1:
    df = data["pv_disc"].sample(min(2000, len(data["pv_disc"])))
    fig = px.scatter(
        df, x="discount_pct", y="profit",
        color="category",
        color_discrete_sequence=[BLUE, GREY_LIGHT, GREY_DARK],
        opacity=0.6,
        labels={"discount_pct": "Discount (%)", "profit": "Profit (USD)"},
    )
    fig.add_hline(y=0, line_dash="dash", line_color=WHITE, opacity=0.3)
    dark_layout(fig, "Profit vs Discount", height=340)
    st.plotly_chart(fig, use_container_width=True)

with r4c2:
    df = data["priority"]
    fig = go.Figure(go.Bar(
        x=df["order_priority"],
        y=df["orders"],
        marker_color=[BLUE, WHITE, GREY_LIGHT, GREY_DARK],
        text=df["orders"],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    dark_layout(fig, "Orders by Priority", height=340)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 5
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("#### Sales & Profit by Region")
df_r = data["region"].copy()
df_r["Sales (USD)"]  = df_r["sales"].apply(lambda v: f"${v:,.0f}")
df_r["Profit (USD)"] = df_r["profit"].apply(lambda v: f"${v:,.0f}")
df_r["Orders"]       = df_r["orders"].apply(lambda v: f"{v:,}")
st.dataframe(
    df_r[["market","region","Sales (USD)","Profit (USD)","Orders"]].rename(
        columns={"market":"Market","region":"Region"}),
    hide_index=True,
    use_container_width=True,
    height=300,
)

