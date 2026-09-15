"""
Page 6: AI Predictor — Klasifikasi (PROFIT/LOSS) + Regresi (Estimasi Profit USD)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.model import predict_classify, predict_regress, whatif_discount_sweep

st.set_page_config(page_title="AI Predictor — StoreIQ", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[data-testid="stApp"]{font-family:'Inter',sans-serif!important;background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('data:image/jpeg;base64,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ta3qq+xrWta3jWta1rem/gt/jW/h941v+QJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAkP/aAAgBAwEBPwFIP//EABQRAQAAAAAAAAAAAAAAAAAAAJD/2gAIAQIBAT8BSD//xAAUEAEAAAAAAAAAAAAAAAAAAACw/9oACAEBAAY/AkWP/8QAHRABAQEBAAIDAQAAAAAAAAAAAAERECAwQFBggP/aAAgBAQABPyHynhERERERE9QAiIlSpWta3utaqqqqq+gBVVVVVXxvuiIiIiIiInpAJUqVKlSta1rWta1rVq1aq9L5gVVVVVVVeX3xE7ERERETxCVKlSpUqVrWta1rWta1rVq1atWrfQAqqqqqqqqvunJyIiIiIiJ4CVKpKlSpUqVrWt43jeNa1q1atWrVKW9Kqqqqqqqqqr74idiIiIiInESpUqVKlSp7wABatWrVq1atW9Kqqqqqqqqq+2InhERERERESpUqVKlSpUqVvmBvoAWrVq1atWrVKqqqqqqvaq++ciIiIiIiIiJUqVKlSpUqVrWta1rWt41rVKatWrVq1atWqqqqqqqqqq/AidiIiIiIiJUqVKlSpUrWta1rW8b01rWtWrVq1atWrVqqqqqqqqqqvviInIiIiIiIiVKlSpUqVK1rWta1rWta1rWtWrVq1atWrVqqqqqqqqqqvvicnYnYiIiclSpUqVrWta1rWta1rWta1rVq1atWrVqqqqqqqqvKq+6InYnIiIiIiIlSpUqVK1rWta1rWta1rWta1a1atWrVqqqqqqqqqqvwpyciIiIiIiclSpUrWta1rWta1rWta1rWrVq1atWrVVVVVVVVVX4c8IiIidiJeytala1rWta1rWta1rWtWtatWrVq1avKqqqqqr8aIiIicnYlSpWta1K1rWta1rWta1rWta1rVq1atVVVVVVVVX48RERE5PDUvNa1rWta1rWta1rWta1rWrVq1avKqqqqvL8meETk8N5Kla1rWta1rWta1rWta1rWta1vN5VVVVV+gnnLzWta1rWta1rWta1rWta1rWtb4VeX6zWta1rWta1rWta1rWta1rWt+21rWta1rWta1rWta1rWta1rW/Z61rWta1rWta1rWta1rWta1v2uta1rWta1rWta1rWta1rW/da1rWta1rWta3mta1rfvNa1rWta1rWta1rfweta1vhrW/xjjOYxjGM5jPwuMYxnhjPw+MYxjGflbyr95PgX7/Wta1rWta1rWta38BrWta1rWta1rW/gta1rWta1rWt/Ea1rW/zD/9oADAMBAAIAAwAAABAb7YppLK9WfZwTV1WZEGvMWH5HUHwwpt2nI5J6JYIo4qap75s3FahnGmNF89LgbP3ZXFFiC9GlLa6boL76LJpKIpNn1JyX9tnv/X+PMvuEqNnyaNWdLJ6o546L666bzuMNUYbzt/xndtvPcsmV8sVy4FUtL5po7o5qZKrozPNNETpJwl8NHn3X1H1vvFSL42Ff7JpoJbKp65Zo7esOU0wLqyEXFu8tN+lHUI4JDUFNfpp7Kr66rL5ps9tOt3SiwZrnEXHEHEDZbbSw3v8Aj3eaOOWCWiKKyenXffbtkkCCy3LzyjTyygg8ppbrrrmay2KCWC++uOfHrzbj/DwUAgUXfXiCuyT/AB220687jjgqvnlughhhr/2y91wwx006xrAGZTx02z22y88okkrlvvuhvsstjm86wy5fQ2nhvvjppkroywzzz3vssjklvtqnhusrrsp274iqlkmDDLHKBIKhunoghjjsrlivvnoqmpshmsrnpqnvvvLBDPcNPKBvljnusqntkqqlvuhrqulpshgssortqjCABXqhLFIEsgijnpkiqrrgvgnloqqumrtnnnusnmpsHPKOENGNPnlpmiqqqtligjuvltqqqqqjtvpvkmjhssDKGBIBOJkiqqqrrluvvvnonngqqqqqqnprnggjhlDENDAJNlqpqqqtlitnsvohrultprq7orqpknAMDDOAHHHFHlllhllkvrgsvohuvguul31319g3vvsMMMJDFLPiqqummiuqlnrgghvtqlt66666+/w/vuvvPPDnvvvqvq6q6qt1gvtiwv/EAB8RAAECBwEBAAAAAAAAAAAAABEAARAgMEBBUGBhcP/aAAgBAwEBPxCwM7PE3T1GeJuXmCCCEjXw042QQ4gREG0oQQgEOHFMdifinmm81OJs2GKn/8QAHBEAAgIDAQEAAAAAAAAAAAAAAREAECAwQFBg/9oACAECAQE/EMxpUUUVKKEaDwChoAtURCIszxDAUIKeJhFKzZ2ixYoUDT2mjtGbxeTp+C44448H1inpduz4D73bjjwccccfhOOOPge5x/AHhODp4CDa/aXyLj+NOkeA8hw//8QAIBABAQEAAgMBAQEBAQAAAAAAAQAQESAwMWFxQVEhQP/aAAgBAQABPxAiIiMER4QP+emUpepS9Sl6lOfqfQA6Bzc6MUpTn7nf3f3K/rH9Sle2/wDd/fSf1hmZv6mZnqRER5AFvZSlKXqXqXeoAhCHUDGPQA5ylOXuUvcvcpe934cBwzLM6REREdAR3DeX6lL1KXrL1dqIIUzPuPu/W79z9zWOg9m17pS9ylKXuU5z9+PAFlmc56EQxgweIGucpS9bX0vtsfXVKU9etcf9w1+8uX65e7pB7pe5e5+5+5zn5OAMyzOkQxER0BHYP8Zc5ynl9r7YfW+t6f8AuBCGB9Y/XUP1MZ9dX3/96de7JS9z9z9znLxwAyzvOnuIjoCI8IG5z9dar0Z/XoqU6g/V+9GfqYx+uyv/AGy92DnOc539dQZ6Bmd5wiGIiMHhAFL1Kc5+svpl6O0qlKZnh/bsG/Xo99r3bS9ylOd/fiADLL0IiIhiI0I7gOUpS8MAKlKUpTp3PoWta/er9dT3dCnOcpX9eIALLO84YRER1A6gpSlKXqXcAD6Yn3H3kp1/++nfvLX7vr4VAKUpSlLxABmWZwiIiIjQwRoRKUpSlDoejD6RCENH7i/q/wCP7n9zp/c/c1r9aH06gClKUpS99gPQLM7zGERDD0BGhhSlKUpSl3AAIQhCEOUdQfrRjGOB7AAUpSlKUpdwFlmZnoRERDzEYMGFKUpSlKUoeoAQhDA6B+r9TodDGPt0A+nQBSlKUpSlLqDMzONzhERERDDgiJSlKUoYZSwGHAhgIQ0HYBjoYxwMe4ABSylKUpS6BZllm/2ehERERDERhSlKUoZQwy6AEIfUYDA+ohgfUYfrDGMYxjGMegD6SlKUpSlKXQMssyzM4REREQxEREpSlKUoZQwwxgGIQhCEIQh2AYxjGMYx6gBSylKUpSlOGZmZ9zMzhEREe4iGGIiUMMMpQyhhhiDoEIQhDQfUdQMYxjGMYxjGMWYspSlKUsMzMyzM9SMPcREMRDDEQwwwyhhhhhhwGIQhCENB4ABjGMYxjGMYssspSylllllmZZZmb/ZnOYjCIiIiIYhhhhhhhhhhhhhiEIQh9RgQh3AMY4MYxjGLLLLLLLLLLLMszMszMszOnQiGIYhj/IYwhhhhhhhhhhhiEIfUQwIT9dBy6B0MYxjGMYsssssssszMzMyzMzMz0I0hiIiIhjBhhhhhhhhiEIQ0Ggho5X60/WHQxjGLLLLLLLLLLLMsyzLMsz0ehERhEREYR05hhhhhhjAhCGgwIdQPYBwYssssstzLLLLMszMzMzMz6nsRERhEMYMaRGDDDcw3MNzodAIdwHOjg4c3NzLcy3OLOssyzLLOMzPuZ6mEREYREdCIeehnMMNzDoeAA/Wn66BbmWWWWW56syzMsyzjM4zM6YdiI00iO5nNzDDc3MPYHNzc9Bzc3MtzjPdmWZmcZ16umGkRhpGDGkRERh15ubm5ubm5ubm5ubm5ubns6zMyzMzLM6zMzOvgIiIiI0iIY099Dxf9689OOiY9mWZZZ16szOOOmGER4SIYiGI0jOLi4uLi4uLi4uLi4uLi4uLj5cXFx0ZmWWZZlmdZmZ1nHHqaaREaRgxDDEMR04uILjTi/EdA/FxpxcXGuMyzLMs92Zn1rr4DDSO5pDEMREfyMC4uLjoDDi4uL8Y4uJLjGZlmWWWWdZmZ1n1rj4TTCNI7kRDDERERBBcYIdQcXFxJJMzMsssszM64zM4z61x7HY00jCIiIjBhhhhhiIiCCCC4uP24uJmZmUspSyyyzLjMzrM4zj346BxhhGGmkdyGGGGGGUMMMMJcw3MssssssspZZZZZZnWZn1OMzjrjic9jDDDDTSNIiIiGGGGGIQhDA6A4MYxjFllll1nozrOuOPROfMYRhHvSPcdubmGGIQ0mf7y5sYxi3MsszMzOs9GcdfBx2MDnDDTSMIjSNGG5udDwkBwW5lx1mcZnWZxn/wBBppGkaYZzc3Nzc3Nzc9gc3Nzc3PRx1mdZnXf54EuPMaaRpph15ubm5ubm5ubm5ubm5uderM9GZz+z1cfIdDDTSNIw6HmOnHZxnWZ1nXHx8f74zCNI008fFxcXFxnFxceJ1mdZ9a469XToYdDDSMI96Rh4D/yuszrOM4++zjv/2Q==') no-repeat center center fixed !important; background-size: cover !important;color:#ffffff!important;}
#MainMenu,footer{visibility:hidden}
[data-testid="stSidebar"]{background:#0a0a0a!important;border-right:1px solid #222222!important;}
.page-header{background:#111111;border-left:4px solid #3b82f6;padding:1.5rem 2rem;margin-bottom:1.5rem;}
.page-header h1{margin:0!important;font-size:1.6rem!important;font-weight:400!important;color:#ffffff;}
.page-header p{color:#888888;margin:0.3rem 0 0;font-size:0.9rem;}
.result-card{background:#111111;border:1px solid #222222;padding:2rem;text-align:center;margin-top:1rem;}
.badge-profit{background:#3b82f6;color:#ffffff;border:1px solid #3b82f6;padding:0.6rem 2rem;font-weight:500;font-size:1.4rem;display:inline-block;letter-spacing:0.05em;}
.badge-loss{background:#333333;color:#ffffff;border:1px solid #444444;padding:0.6rem 2rem;font-weight:500;font-size:1.4rem;display:inline-block;letter-spacing:0.05em;}
.pred-usd{font-size:2.8rem;font-weight:400;}
.conf-text{color:#888888;font-size:0.9rem;margin-top:0.4rem;text-transform:uppercase;letter-spacing:0.05em;}
.stButton>button{background: #1d4ed8 !important;color: #ffffff !important;border:none!important;border-radius:0!important;font-weight:500!important;font-size:1rem!important;padding:0.6rem 2rem!important;transition:opacity 0.2s!important;}
.stButton>button p { color: #ffffff !important; }
.stButton>button:hover{opacity:0.8!important;}
hr{border-color:#222222!important;}
.input-section{background:#111111;border:1px solid #222222;padding:1.4rem 1.6rem;margin-bottom:1rem;}
[data-testid="stSelectbox"] > div, [data-testid="stTextInput"] > div > input, [data-testid="stNumberInput"] > div > input { background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('data:image/jpeg;base64,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ta3qq+xrWta3jWta1rem/gt/jW/h941v+QJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAkP/aAAgBAwEBPwFIP//EABQRAQAAAAAAAAAAAAAAAAAAAJD/2gAIAQIBAT8BSD//xAAUEAEAAAAAAAAAAAAAAAAAAACw/9oACAEBAAY/AkWP/8QAHRABAQEBAAIDAQAAAAAAAAAAAAERECAwQFBggP/aAAgBAQABPyHynhERERERE9QAiIlSpWta3utaqqqqq+gBVVVVVXxvuiIiIiIiInpAJUqVKlSta1rWta1rVq1aq9L5gVVVVVVVeX3xE7ERERETxCVKlSpUqVrWta1rWta1rVq1atWrfQAqqqqqqqqvunJyIiIiIiJ4CVKpKlSpUqVrWt43jeNa1q1atWrVKW9Kqqqqqqqqqr74idiIiIiInESpUqVKlSp7wABatWrVq1atW9Kqqqqqqqqq+2InhERERERESpUqVKlSpUqVvmBvoAWrVq1atWrVKqqqqqqvaq++ciIiIiIiIiJUqVKlSpUqVrWta1rWt41rVKatWrVq1atWqqqqqqqqqq/AidiIiIiIiJUqVKlSpUrWta1rW8b01rWtWrVq1atWrVqqqqqqqqqqvviInIiIiIiIiVKlSpUqVK1rWta1rWta1rWtWrVq1atWrVqqqqqqqqqqvvicnYnYiIiclSpUqVrWta1rWta1rWta1rVq1atWrVqqqqqqqqvKq+6InYnIiIiIiIlSpUqVK1rWta1rWta1rWta1a1atWrVqqqqqqqqqqvwpyciIiIiIiclSpUrWta1rWta1rWta1rWrVq1atWrVVVVVVVVVX4c8IiIidiJeytala1rWta1rWta1rWtWtatWrVq1avKqqqqqr8aIiIicnYlSpWta1K1rWta1rWta1rWta1rVq1atVVVVVVVVX48RERE5PDUvNa1rWta1rWta1rWta1rWrVq1avKqqqqvL8meETk8N5Kla1rWta1rWta1rWta1rWta1vN5VVVVV+gnnLzWta1rWta1rWta1rWta1rWtb4VeX6zWta1rWta1rWta1rWta1rWt+21rWta1rWta1rWta1rWta1rW/Z61rWta1rWta1rWta1rWta1v2uta1rWta1rWta1rWta1rW/da1rWta1rWta3mta1rfvNa1rWta1rWta1rfweta1vhrW/xjjOYxjGM5jPwuMYxnhjPw+MYxjGflbyr95PgX7/Wta1rWta1rWta38BrWta1rWta1rW/gta1rWta1rWt/Ea1rW/zD/9oADAMBAAIAAwAAABAb7YppLK9WfZwTV1WZEGvMWH5HUHwwpt2nI5J6JYIo4qap75s3FahnGmNF89LgbP3ZXFFiC9GlLa6boL76LJpKIpNn1JyX9tnv/X+PMvuEqNnyaNWdLJ6o546L666bzuMNUYbzt/xndtvPcsmV8sVy4FUtL5po7o5qZKrozPNNETpJwl8NHn3X1H1vvFSL42Ff7JpoJbKp65Zo7esOU0wLqyEXFu8tN+lHUI4JDUFNfpp7Kr66rL5ps9tOt3SiwZrnEXHEHEDZbbSw3v8Aj3eaOOWCWiKKyenXffbtkkCCy3LzyjTyygg8ppbrrrmay2KCWC++uOfHrzbj/DwUAgUXfXiCuyT/AB220687jjgqvnlughhhr/2y91wwx006xrAGZTx02z22y88okkrlvvuhvsstjm86wy5fQ2nhvvjppkroywzzz3vssjklvtqnhusrrsp274iqlkmDDLHKBIKhunoghjjsrlivvnoqmpshmsrnpqnvvvLBDPcNPKBvljnusqntkqqlvuhrqulpshgssortqjCABXqhLFIEsgijnpkiqrrgvgnloqqumrtnnnusnmpsHPKOENGNPnlpmiqqqtligjuvltqqqqqjtvpvkmjhssDKGBIBOJkiqqqrrluvvvnonngqqqqqqnprnggjhlDENDAJNlqpqqqtlitnsvohrultprq7orqpknAMDDOAHHHFHlllhllkvrgsvohuvguul31319g3vvsMMMJDFLPiqqummiuqlnrgghvtqlt66666+/w/vuvvPPDnvvvqvq6q6qt1gvtiwv/EAB8RAAECBwEBAAAAAAAAAAAAABEAARAgMEBBUGBhcP/aAAgBAwEBPxCwM7PE3T1GeJuXmCCCEjXw042QQ4gREG0oQQgEOHFMdifinmm81OJs2GKn/8QAHBEAAgIDAQEAAAAAAAAAAAAAAREAECAwQFBg/9oACAECAQE/EMxpUUUVKKEaDwChoAtURCIszxDAUIKeJhFKzZ2ixYoUDT2mjtGbxeTp+C44448H1inpduz4D73bjjwccccfhOOOPge5x/AHhODp4CDa/aXyLj+NOkeA8hw//8QAIBAB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') no-repeat center center fixed !important; background-size: cover !important; border: 1px solid #333333 !important; color: #ffffff !important; border-radius: 0 !important; }
[data-testid="stTabs"] button { color: #888888 !important; font-weight: 400 !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }
[data-testid="stSlider"] [data-testid="stSlider"] { color: #3b82f6 !important; }
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

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>AI Predictor</h1>
    <p>XGBoost-powered prediction: Profit/Loss Status & USD Profit Estimation</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INPUT FORM (shared untuk kedua model)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Transaction Parameters")

with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)

    row1 = st.columns(4)
    sales         = row1[0].number_input("Sales (USD)",         min_value=0.01, max_value=100000.0, value=250.0, step=10.0, format="%.2f")
    discount_pct  = row1[1].number_input("Discount (%)",          min_value=0.0,  max_value=100.0,   value=10.0,  step=1.0,  format="%.1f")
    shipping_cost = row1[2].number_input("Shipping Cost (USD)",   min_value=0.0,  max_value=5000.0,  value=15.0,  step=1.0,  format="%.2f")
    quantity      = row1[3].number_input("Quantity",            min_value=1,    max_value=100,     value=3,     step=1)

    row2 = st.columns(4)
    category = row2[0].selectbox("Category", ["Furniture", "Office Supplies", "Technology"])
    SUB_BY_CAT = {
        "Furniture":       ["Bookcases","Chairs","Furnishings","Tables"],
        "Office Supplies": ["Appliances","Art","Binders","Envelopes","Fasteners","Labels","Paper","Storage","Supplies"],
        "Technology":      ["Accessories","Copiers","Machines","Phones"],
    }
    sub_category  = row2[1].selectbox("Sub-Category", SUB_BY_CAT[category])
    segment       = row2[2].selectbox("Segment",     ["Consumer","Corporate","Home Office"])
    market        = row2[3].selectbox("Market",      ["APAC","Africa","Canada","EMEA","EU","LATAM","US"])

    row3 = st.columns(3)
    ship_mode      = row3[0].selectbox("Ship Mode",       ["First Class","Same Day","Second Class","Standard Class"])
    order_priority = row3[1].selectbox("Order Priority",  ["Critical","High","Low","Medium"])
    region         = row3[2].selectbox("Region",          [
        "Africa","Canada","Caribbean","Central","Central Asia",
        "EMEA","East","North","North Asia","Oceania","South",
        "Southeast Asia","West"
    ])

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS: Klasifikasi vs Regresi
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
tab_clf, tab_reg, tab_whatif = st.tabs([
    "Status Detector",
    "Profit Estimator",
    "What-If Analysis",
])

# ── Build common kwargs ────────────────────────────────────────────────────────
common_kwargs = dict(
    sales=sales, discount_pct=discount_pct, shipping_cost=shipping_cost,
    quantity=quantity, category=category, sub_category=sub_category,
    segment=segment, market=market, ship_mode=ship_mode,
    order_priority=order_priority, region=region,
)

BLUE = "#3b82f6"
GREY_D = "#444444"
WHITE = "#ffffff"

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: KLASIFIKASI
# ─────────────────────────────────────────────────────────────────────────────
with tab_clf:
    st.markdown("#### Predict Transaction Status: PROFIT or LOSS")
    st.markdown("XGBoost Classifier model trained on Global Superstore dataset.")

    col_btn, col_empty = st.columns([1, 3])
    predict_clf = col_btn.button("Predict Status", key="btn_clf", use_container_width=True)

    if predict_clf:
        with st.spinner("Running classification model..."):
            try:
                result = predict_classify(**common_kwargs)

                label      = result["label"]
                confidence = result["confidence"] * 100
                prob_profit = result["prob_profit"] * 100
                prob_loss   = result["prob_loss"] * 100

                r1, r2, r3 = st.columns([1, 1.2, 1])

                with r1:
                    badge_cls = "badge-profit" if label == "PROFIT" else "badge-loss"
                    color     = BLUE if label == "PROFIT" else WHITE
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="conf-text">PREDICTED STATUS</div>
                        <div style="margin:1rem 0">
                            <span class="{badge_cls}">{label}</span>
                        </div>
                        <div class="conf-text">Confidence: <strong style="color:{color}">{confidence:.1f}%</strong></div>
                    </div>
                    """, unsafe_allow_html=True)

                with r2:
                    fig = go.Figure(go.Bar(
                        x=["PROFIT","LOSS"],
                        y=[prob_profit, prob_loss],
                        marker_color=[BLUE, GREY_D],
                        text=[f"{prob_profit:.1f}%", f"{prob_loss:.1f}%"],
                        textposition="outside",
                        textfont=dict(color=WHITE, size=12, family="Inter"),
                        width=0.5,
                    ))
                    fig.update_layout(
                        plot_bgcolor="#111111", paper_bgcolor="#111111",
                        font=dict(family="Inter", color="#888888"),
                        margin=dict(l=16,r=16,t=40,b=16), height=260,
                        showlegend=False,
                        xaxis=dict(gridcolor="rgba(0,0,0,0)", linecolor="#333333"),
                        yaxis=dict(range=[0,110], gridcolor="#1a1a1a", linecolor="#333333"),
                        title=dict(text="Probability Distribution", font=dict(color=WHITE,size=12,weight="normal"), x=0.5, xanchor="center"),
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with r3:
                    gross_profit_est = sales * (1 - discount_pct/100) - shipping_cost
                    margin_est = (gross_profit_est / sales * 100) if sales > 0 else 0
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="conf-text">INPUT SUMMARY</div>
                        <table style="width:100%;margin-top:0.8rem;font-size:0.85rem;text-align:left">
                        <tr><td style="color:#888888;padding:4px 0">Sales</td><td style="color:#ffffff;text-align:right"><b>${sales:,.2f}</b></td></tr>
                        <tr><td style="color:#888888;padding:4px 0">Discount</td><td style="color:#ffffff;text-align:right"><b>{discount_pct:.1f}%</b></td></tr>
                        <tr><td style="color:#888888;padding:4px 0">Ship Cost</td><td style="color:#ffffff;text-align:right"><b>${shipping_cost:,.2f}</b></td></tr>
                        <tr><td style="color:#888888;padding:4px 0">Qty</td><td style="color:#ffffff;text-align:right"><b>{quantity}</b></td></tr>
                        <tr><td style="color:#888888;padding:4px 0">Est. Margin</td><td style="color:{BLUE if margin_est>0 else WHITE};text-align:right"><b>{margin_est:.1f}%</b></td></tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Input parameters above and click **Predict Status**.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: REGRESI
# ─────────────────────────────────────────────────────────────────────────────
with tab_reg:
    st.markdown("#### Estimate USD Profit Margin")
    st.markdown("XGBoost Regressor model predicts the estimated profit value in USD.")

    col_btn2, col_empty2 = st.columns([1, 3])
    predict_reg = col_btn2.button("Estimate Profit", key="btn_reg", use_container_width=True)

    if predict_reg:
        with st.spinner("Running regression model..."):
            try:
                result = predict_regress(**common_kwargs)
                pred_profit = result["predicted_profit"]
                status      = result["status"]

                color    = BLUE if status == "PROFIT" else WHITE
                sign     = "+" if pred_profit >= 0 else ""
                badge_cls = "badge-profit" if status == "PROFIT" else "badge-loss"

                r1, r2 = st.columns([1, 1.5])

                with r1:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="conf-text">ESTIMATED PROFIT</div>
                        <div class="pred-usd" style="color:{color};margin:1rem 0">{sign}${pred_profit:,.2f}</div>
                        <div style="margin:0.5rem 0">
                            <span class="{badge_cls}">{status}</span>
                        </div>
                        <div class="conf-text" style="margin-top:0.8rem;text-transform:none">
                            Sales: ${sales:,.2f} | Disc: {discount_pct:.1f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with r2:
                    max_val = max(abs(pred_profit) * 2, 500)
                    gauge_color = BLUE if pred_profit >= 0 else GREY_D
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=pred_profit,
                        delta={"reference": 0, "increasing": {"color": BLUE}, "decreasing": {"color": GREY_D}},
                        number={"prefix": "$", "font": {"size": 36, "color": WHITE, "family": "Inter"}},
                        gauge={
                            "axis": {"range": [-max_val, max_val], "tickcolor": "#333333",
                                     "tickfont": {"color": "#888888"}},
                            "bar": {"color": gauge_color, "thickness": 0.3},
                            "bgcolor": "#111111",
                            "bordercolor": "#222222",
                            "steps": [
                                {"range": [-max_val, 0], "color": "#1a1a1a"},
                                {"range": [0, max_val], "color": "#222222"},
                            ],
                            "threshold": {"line": {"color": WHITE,"width": 2}, "thickness": 0.75, "value": 0},
                        },
                        title={"text": "Estimated Profit (USD)", "font": {"color": WHITE, "size": 13, "weight":"normal"}},
                    ))
                    fig.update_layout(
                        paper_bgcolor="#111111", font=dict(color="#888888", family="Inter"),
                        margin=dict(l=20,r=20,t=60,b=20), height=300,
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Input parameters above and click **Estimate Profit**.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: WHAT-IF ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab_whatif:
    st.markdown("#### What-If Analysis: Discount Impact on Profit")
    st.markdown("Simulate how changing the **discount rate** affects estimated profit, keeping other parameters constant.")

    wc1, wc2, wc3 = st.columns(3)
    disc_min  = wc1.slider("Min Discount (%)", 0, 50,  0)
    disc_max  = wc2.slider("Max Discount (%)", 10, 90, 80)
    steps     = wc3.slider("Number of Steps", 10, 50, 20)

    col_btn3, _ = st.columns([1, 3])
    run_whatif = col_btn3.button("Run Analysis", key="btn_whatif", use_container_width=True)

    if run_whatif:
        if disc_min >= disc_max:
            st.warning("Min discount must be less than max discount.")
        else:
            with st.spinner("Running simulation..."):
                try:
                    df_wi = whatif_discount_sweep(
                        sales=sales, shipping_cost=shipping_cost, quantity=quantity,
                        category=category, sub_category=sub_category,
                        segment=segment, market=market, ship_mode=ship_mode,
                        order_priority=order_priority, region=region,
                        discount_range=(disc_min, disc_max), steps=steps,
                    )

                    colors = [BLUE if v >= 0 else GREY_D for v in df_wi["predicted_profit"]]

                    fig = go.Figure()
                    fig.add_scatter(
                        x=df_wi["discount_pct"], y=df_wi["predicted_profit"],
                        mode="lines+markers",
                        line=dict(color="#666666", width=2),
                        marker=dict(color=colors, size=8, line=dict(color="#000000", width=1)),
                        name="Estimated Profit",
                    )
                    fig.add_hline(y=0, line_dash="dash", line_color=WHITE, opacity=0.4,
                                  annotation_text="Break-even", annotation_font_color=WHITE)
                    fig.update_layout(
                        plot_bgcolor="#111111", paper_bgcolor="#111111",
                        font=dict(family="Inter", color="#888888", size=11),
                        title=dict(text=f"Profit vs Discount — Sales=${sales:.0f}, Qty={quantity}, Ship=${shipping_cost:.0f}",
                                   font=dict(color=WHITE,size=13,weight="normal"), x=0.02),
                        xaxis=dict(title="Discount (%)", gridcolor="#1a1a1a", linecolor="#333333"),
                        yaxis=dict(title="Estimated Profit (USD)", gridcolor="#1a1a1a", linecolor="#333333"),
                        margin=dict(l=16,r=16,t=50,b=16), height=380,
                        showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    df_pos = df_wi[df_wi["predicted_profit"] >= 0]
                    if not df_pos.empty:
                        max_safe_disc = df_pos["discount_pct"].max()
                        st.success(f"Maximum safe discount before loss: **{max_safe_disc:.1f}%**")
                    else:
                        st.error("Entire discount range results in LOSS for these parameters.")

                    with st.expander("View Simulation Data"):
                        df_wi_display = df_wi.copy()
                        df_wi_display["Status"] = df_wi_display["predicted_profit"].apply(lambda v: "PROFIT" if v >= 0 else "LOSS")
                        df_wi_display["discount_pct"] = df_wi_display["discount_pct"].round(1)
                        df_wi_display["predicted_profit"] = df_wi_display["predicted_profit"].round(2)
                        st.dataframe(df_wi_display.rename(columns={"discount_pct":"Discount (%)","predicted_profit":"Est. Profit (USD)"}),
                                     hide_index=True, use_container_width=True)

                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Set discount range and click **Run Analysis**.")

# ── Footer info ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#666666;font-size:0.75rem;padding:0.5rem 0">
    Powered by <strong>XGBoost</strong> •
    Classification: <strong>Binary (Profit/Loss)</strong> •
    Regression: <strong>Profit USD</strong>
</div>
""", unsafe_allow_html=True)





