"""
Script untuk rebuild scaler dari data SQLite karena pickle scaler tidak kompatibel
dengan versi Python/sklearn saat ini.
Jalankan sekali: python rebuild_scalers.py
"""
import sqlite3, os, pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE    = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE, "superstore (1).sqlite")

# ── Load data dari SQLite ─────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("""
    SELECT
        oi.sales, oi.discount, oi.quantity, oi.shipping_cost,
        oi.profit,
        o.ship_mode, o.order_priority,
        c.segment,
        l.market, l.region,
        p.category, p.sub_category
    FROM order_items oi
    JOIN orders o      ON oi.order_key  = o.order_key
    JOIN dim_customers c ON o.customer_id = c.customer_id
    JOIN dim_locations l ON o.location_id = l.location_id
    JOIN dim_products  p ON oi.product_id  = p.product_id
""", conn)
conn.close()

print(f"Loaded {len(df)} rows from DB")

# ── Feature engineering (sama persis dengan model.py) ────────────────────────
df["discount_impact"]      = df["discount"] * df["sales"]
df["shipping_cost_ratio"]  = df["shipping_cost"] / df["sales"].replace(0, np.nan)
df["shipping_cost_ratio"]  = df["shipping_cost_ratio"].fillna(0)
df["total_cost_spent"]     = df["sales"] + df["shipping_cost"]

# One-hot encoding
ohe_cols = {
    "ship_mode":      ["Same Day", "Second Class", "Standard Class"],
    "order_priority": ["High", "Low", "Medium"],
    "segment":        ["Corporate", "Home Office"],
    "market":         ["Africa", "Canada", "EMEA", "EU", "LATAM", "US"],
    "region":         ["Canada","Caribbean","Central","Central Asia","EMEA","East","North","North Asia","Oceania","South","Southeast Asia","West"],
    "category":       ["Office Supplies", "Technology"],
    "sub_category":   ["Appliances","Art","Binders","Bookcases","Chairs","Copiers","Envelopes","Fasteners","Furnishings","Labels","Machines","Paper","Phones","Storage","Supplies","Tables"],
}

for col, values in ohe_cols.items():
    for v in values:
        col_name = f"{col}_{v}"
        df[col_name] = (df[col] == v).astype(int)

# ── Load training columns dari pkl (sudah berhasil dibaca) ────────────────────
with open(os.path.join(BASE, "model_klasifikasi", "training_columns_clf.pkl"), "rb") as f:
    clf_cols = pickle.load(f)

with open(os.path.join(BASE, "model_regresi", "training_columns_reg.pkl"), "rb") as f:
    reg_cols = pickle.load(f)

print("CLF cols:", clf_cols[:5], "...")
print("REG cols:", reg_cols[:5], "...")

# Align columns
X_clf = df.reindex(columns=clf_cols, fill_value=0)
X_reg = df.reindex(columns=reg_cols, fill_value=0)

print(f"X_clf shape: {X_clf.shape}")
print(f"X_reg shape: {X_reg.shape}")

# ── Fit new scalers ───────────────────────────────────────────────────────────
scaler_clf = StandardScaler()
scaler_clf.fit(X_clf)

scaler_reg = StandardScaler()
scaler_reg.fit(X_reg)

# ── Save new scalers ──────────────────────────────────────────────────────────
with open(os.path.join(BASE, "model_klasifikasi", "scaler_clf.pkl"), "wb") as f:
    pickle.dump(scaler_clf, f, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(BASE, "model_regresi", "scaler_reg.pkl"), "wb") as f:
    pickle.dump(scaler_reg, f, protocol=pickle.HIGHEST_PROTOCOL)

print("\n✅ Scalers rebuilt and saved successfully!")
print(f"   - model_klasifikasi/scaler_clf.pkl")
print(f"   - model_regresi/scaler_reg.pkl")

# ── Quick verification ────────────────────────────────────────────────────────
test_row = X_clf.iloc[:1]
scaled = scaler_clf.transform(test_row)
print(f"\nVerification — scaled shape: {scaled.shape}, mean range: [{scaled.min():.2f}, {scaled.max():.2f}]")
