import os
import pickle
import numpy as np
import pandas as pd

# ─── Paths ──────────────────────────────────────────────────────────────────
_APP_DIR    = os.path.dirname(os.path.dirname(__file__))   # streamlit_app/
_PARENT_DIR = os.path.dirname(_APP_DIR)                    # LnTCamp 2026/

def _find_dir(name):
    """Find model dir: streamlit_app/name first, then parent/name."""
    candidate = os.path.join(_APP_DIR, name)
    if os.path.isdir(candidate):
        return candidate
    return os.path.join(_PARENT_DIR, name)

CLF_MODEL_PATH = os.path.join(_find_dir("model_klasifikasi"), "xgboost_clf_model.pkl")
CLF_SCALER_PATH = os.path.join(_find_dir("model_klasifikasi"), "scaler_clf.pkl")
CLF_COLS_PATH = os.path.join(_find_dir("model_klasifikasi"), "training_columns_clf.pkl")

REG_MODEL_PATH = os.path.join(_find_dir("model_regresi"), "xgboost_reg_model.pkl")
REG_SCALER_PATH = os.path.join(_find_dir("model_regresi"), "scaler_reg.pkl")
REG_COLS_PATH = os.path.join(_find_dir("model_regresi"), "training_columns_reg.pkl")



def _load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


# ─── Lazy-load models (cached at module level) ───────────────────────────────
_clf_model = None
_clf_scaler = None
_clf_cols = None
_reg_model = None
_reg_scaler = None
_reg_cols = None


def load_clf():
    global _clf_model, _clf_scaler, _clf_cols
    if _clf_model is None:
        _clf_model = _load_pickle(CLF_MODEL_PATH)
        _clf_scaler = _load_pickle(CLF_SCALER_PATH)
        _clf_cols = _load_pickle(CLF_COLS_PATH)
    return _clf_model, _clf_scaler, _clf_cols


def load_reg():
    global _reg_model, _reg_scaler, _reg_cols
    if _reg_model is None:
        _reg_model = _load_pickle(REG_MODEL_PATH)
        _reg_scaler = _load_pickle(REG_SCALER_PATH)
        _reg_cols = _load_pickle(REG_COLS_PATH)
    return _reg_model, _reg_scaler, _reg_cols


# ─── Feature Engineering ────────────────────────────────────────────────────

def build_features(
    sales: float,
    discount_pct: float,
    shipping_cost: float,
    quantity: int,
    category: str,
    sub_category: str,
    segment: str,
    market: str,
    ship_mode: str,
    order_priority: str,
    region: str,
) -> pd.DataFrame:
    """
    Build a single-row feature DataFrame sesuai training columns.
    discount_pct dalam format 0-100 (akan di-convert ke 0-1).
    """
    discount = discount_pct / 100.0

    # Derived features
    shipping_cost_ratio = shipping_cost / sales if sales > 0 else 0.0
    discount_impact = discount * sales
    total_cost_spent = sales + shipping_cost

    # Base numeric row
    row = {
        "sales": sales,
        "discount": discount,
        "quantity": quantity,
        "shipping_cost": shipping_cost,
        "shipping_cost_ratio": shipping_cost_ratio,
        "discount_impact": discount_impact,
        "total_cost_spent": total_cost_spent,
    }

    # One-hot encoded fields (all default 0)
    ohe_fields = {
        # ship_mode (base = First Class)
        "ship_mode_Same Day": 1 if ship_mode == "Same Day" else 0,
        "ship_mode_Second Class": 1 if ship_mode == "Second Class" else 0,
        "ship_mode_Standard Class": 1 if ship_mode == "Standard Class" else 0,
        # order_priority (base = Critical)
        "order_priority_High": 1 if order_priority == "High" else 0,
        "order_priority_Low": 1 if order_priority == "Low" else 0,
        "order_priority_Medium": 1 if order_priority == "Medium" else 0,
        # segment (base = Consumer)
        "segment_Corporate": 1 if segment == "Corporate" else 0,
        "segment_Home Office": 1 if segment == "Home Office" else 0,
        # market (base = APAC)
        "market_Africa": 1 if market == "Africa" else 0,
        "market_Canada": 1 if market == "Canada" else 0,
        "market_EMEA": 1 if market == "EMEA" else 0,
        "market_EU": 1 if market == "EU" else 0,
        "market_LATAM": 1 if market == "LATAM" else 0,
        "market_US": 1 if market == "US" else 0,
        # region (base = Africa)
        "region_Canada": 1 if region == "Canada" else 0,
        "region_Caribbean": 1 if region == "Caribbean" else 0,
        "region_Central": 1 if region == "Central" else 0,
        "region_Central Asia": 1 if region == "Central Asia" else 0,
        "region_EMEA": 1 if region == "EMEA" else 0,
        "region_East": 1 if region == "East" else 0,
        "region_North": 1 if region == "North" else 0,
        "region_North Asia": 1 if region == "North Asia" else 0,
        "region_Oceania": 1 if region == "Oceania" else 0,
        "region_South": 1 if region == "South" else 0,
        "region_Southeast Asia": 1 if region == "Southeast Asia" else 0,
        "region_West": 1 if region == "West" else 0,
        # category (base = Furniture)
        "category_Office Supplies": 1 if category == "Office Supplies" else 0,
        "category_Technology": 1 if category == "Technology" else 0,
        # sub_category (base = Accessories)
        "sub_category_Appliances": 1 if sub_category == "Appliances" else 0,
        "sub_category_Art": 1 if sub_category == "Art" else 0,
        "sub_category_Binders": 1 if sub_category == "Binders" else 0,
        "sub_category_Bookcases": 1 if sub_category == "Bookcases" else 0,
        "sub_category_Chairs": 1 if sub_category == "Chairs" else 0,
        "sub_category_Copiers": 1 if sub_category == "Copiers" else 0,
        "sub_category_Envelopes": 1 if sub_category == "Envelopes" else 0,
        "sub_category_Fasteners": 1 if sub_category == "Fasteners" else 0,
        "sub_category_Furnishings": 1 if sub_category == "Furnishings" else 0,
        "sub_category_Labels": 1 if sub_category == "Labels" else 0,
        "sub_category_Machines": 1 if sub_category == "Machines" else 0,
        "sub_category_Paper": 1 if sub_category == "Paper" else 0,
        "sub_category_Phones": 1 if sub_category == "Phones" else 0,
        "sub_category_Storage": 1 if sub_category == "Storage" else 0,
        "sub_category_Supplies": 1 if sub_category == "Supplies" else 0,
        "sub_category_Tables": 1 if sub_category == "Tables" else 0,
    }

    row.update(ohe_fields)
    df = pd.DataFrame([row])
    return df


def _align_to_cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Reindex to match exact training columns, fill missing with 0."""
    return df.reindex(columns=cols, fill_value=0)


# ─── Predict Functions ───────────────────────────────────────────────────────

def predict_classify(
    sales, discount_pct, shipping_cost, quantity,
    category, sub_category, segment, market,
    ship_mode, order_priority, region
) -> dict:
    """
    Returns dict:
        label     : 'PROFIT' | 'LOSS'
        confidence: float 0-1
        prob_profit: float
        prob_loss  : float
    """
    model, scaler, cols = load_clf()
    df = build_features(
        sales, discount_pct, shipping_cost, quantity,
        category, sub_category, segment, market,
        ship_mode, order_priority, region
    )
    df = _align_to_cols(df, cols)
    X_scaled = scaler.transform(df)
    pred = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0]

    # class 1 = profit (positive), class 0 = loss
    prob_profit = float(proba[1]) if proba.shape[0] > 1 else float(proba[0])
    prob_loss = 1.0 - prob_profit

    return {
        "label": "PROFIT" if pred == 1 else "LOSS",
        "confidence": max(prob_profit, prob_loss),
        "prob_profit": prob_profit,
        "prob_loss": prob_loss,
        "raw_pred": int(pred),
    }


def predict_regress(
    sales, discount_pct, shipping_cost, quantity,
    category, sub_category, segment, market,
    ship_mode, order_priority, region
) -> dict:
    """
    Returns dict:
        predicted_profit: float (USD)
        status          : 'PROFIT' | 'LOSS'
    """
    model, scaler, cols = load_reg()
    df = build_features(
        sales, discount_pct, shipping_cost, quantity,
        category, sub_category, segment, market,
        ship_mode, order_priority, region
    )
    df = _align_to_cols(df, cols)
    X_scaled = scaler.transform(df)
    pred_profit = float(model.predict(X_scaled)[0])

    return {
        "predicted_profit": pred_profit,
        "status": "PROFIT" if pred_profit >= 0 else "LOSS",
    }


def whatif_discount_sweep(
    sales, shipping_cost, quantity,
    category, sub_category, segment, market,
    ship_mode, order_priority, region,
    discount_range=(0, 80), steps=20
) -> pd.DataFrame:
    """
    Sweep diskon dari min ke max dan return DataFrame profit estimate.
    Berguna untuk What-If Analysis chart.
    """
    discounts = np.linspace(discount_range[0], discount_range[1], steps)
    results = []
    for d in discounts:
        r = predict_regress(
            sales, d, shipping_cost, quantity,
            category, sub_category, segment, market,
            ship_mode, order_priority, region
        )
        results.append({"discount_pct": d, "predicted_profit": r["predicted_profit"]})
    return pd.DataFrame(results)
