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
html, body, [data-testid="stApp"] { font-family:'Inter',sans-serif!important; background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('data:image/jpeg;base64,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ta3qq+xrWta3jWta1rem/gt/jW/h941v+QJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAkP/aAAgBAwEBPwFIP//EABQRAQAAAAAAAAAAAAAAAAAAAJD/2gAIAQIBAT8BSD//xAAUEAEAAAAAAAAAAAAAAAAAAACw/9oACAEBAAY/AkWP/8QAHRABAQEBAAIDAQAAAAAAAAAAAAERECAwQFBggP/aAAgBAQABPyHynhERERERE9QAiIlSpWta3utaqqqqq+gBVVVVVXxvuiIiIiIiInpAJUqVKlSta1rWta1rVq1aq9L5gVVVVVVVeX3xE7ERERETxCVKlSpUqVrWta1rWta1rVq1atWrfQAqqqqqqqqvunJyIiIiIiJ4CVKpKlSpUqVrWt43jeNa1q1atWrVKW9Kqqqqqqqqqr74idiIiIiInESpUqVKlSp7wABatWrVq1atW9Kqqqqqqqqq+2InhERERERESpUqVKlSpUqVvmBvoAWrVq1atWrVKqqqqqqvaq++ciIiIiIiIiJUqVKlSpUqVrWta1rWt41rVKatWrVq1atWqqqqqqqqqq/AidiIiIiIiJUqVKlSpUrWta1rW8b01rWtWrVq1atWrVqqqqqqqqqqvviInIiIiIiIiVKlSpUqVK1rWta1rWta1rWtWrVq1atWrVqqqqqqqqqqvvicnYnYiIiclSpUqVrWta1rWta1rWta1rVq1atWrVqqqqqqqqvKq+6InYnIiIiIiIlSpUqVK1rWta1rWta1rWta1a1atWrVqqqqqqqqqqvwpyciIiIiIiclSpUrWta1rWta1rWta1rWrVq1atWrVVVVVVVVVX4c8IiIidiJeytala1rWta1rWta1rWtWtatWrVq1avKqqqqqr8aIiIicnYlSpWta1K1rWta1rWta1rWta1rVq1atVVVVVVVVX48RERE5PDUvNa1rWta1rWta1rWta1rWrVq1avKqqqqvL8meETk8N5Kla1rWta1rWta1rWta1rWta1vN5VVVVV+gnnLzWta1rWta1rWta1rWta1rWtb4VeX6zWta1rWta1rWta1rWta1rWt+21rWta1rWta1rWta1rWta1rW/Z61rWta1rWta1rWta1rWta1v2uta1rWta1rWta1rWta1rW/da1rWta1rWta3mta1rfvNa1rWta1rWta1rfweta1vhrW/xjjOYxjGM5jPwuMYxnhjPw+MYxjGflbyr95PgX7/Wta1rWta1rWta38BrWta1rWta1rW/gta1rWta1rWt/Ea1rW/zD/9oADAMBAAIAAwAAABAb7YppLK9WfZwTV1WZEGvMWH5HUHwwpt2nI5J6JYIo4qap75s3FahnGmNF89LgbP3ZXFFiC9GlLa6boL76LJpKIpNn1JyX9tnv/X+PMvuEqNnyaNWdLJ6o546L666bzuMNUYbzt/xndtvPcsmV8sVy4FUtL5po7o5qZKrozPNNETpJwl8NHn3X1H1vvFSL42Ff7JpoJbKp65Zo7esOU0wLqyEXFu8tN+lHUI4JDUFNfpp7Kr66rL5ps9tOt3SiwZrnEXHEHEDZbbSw3v8Aj3eaOOWCWiKKyenXffbtkkCCy3LzyjTyygg8ppbrrrmay2KCWC++uOfHrzbj/DwUAgUXfXiCuyT/AB220687jjgqvnlughhhr/2y91wwx006xrAGZTx02z22y88okkrlvvuhvsstjm86wy5fQ2nhvvjppkroywzzz3vssjklvtqnhusrrsp274iqlkmDDLHKBIKhunoghjjsrlivvnoqmpshmsrnpqnvvvLBDPcNPKBvljnusqntkqqlvuhrqulpshgssortqjCABXqhLFIEsgijnpkiqrrgvgnloqqumrtnnnusnmpsHPKOENGNPnlpmiqqqtligjuvltqqqqqjtvpvkmjhssDKGBIBOJkiqqqrrluvvvnonngqqqqqqnprnggjhlDENDAJNlqpqqqtlitnsvohrultprq7orqpknAMDDOAHHHFHlllhllkvrgsvohuvguul31319g3vvsMMMJDFLPiqqummiuqlnrgghvtqlt66666+/w/vuvvPPDnvvvqvq6q6qt1gvtiwv/EAB8RAAECBwEBAAAAAAAAAAAAABEAARAgMEBBUGBhcP/aAAgBAwEBPxCwM7PE3T1GeJuXmCCCEjXw042QQ4gREG0oQQgEOHFMdifinmm81OJs2GKn/8QAHBEAAgIDAQEAAAAAAAAAAAAAAREAECAwQFBg/9oACAECAQE/EMxpUUUVKKEaDwChoAtURCIszxDAUIKeJhFKzZ2ixYoUDT2mjtGbxeTp+C44448H1inpduz4D73bjjwccccfhOOOPge5x/AHhODp4CDa/aXyLj+NOkeA8hw//8QAIBAB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') no-repeat center center fixed !important; background-size: cover !important; color:#ffffff!important; }
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





