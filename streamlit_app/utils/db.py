import sqlite3
import pandas as pd
import os

# Path ke database — dicari dari utils/ naik ke streamlit_app/, lalu ke parent juga sebagai fallback
_APP_DIR = os.path.dirname(os.path.dirname(__file__))   # streamlit_app/
_PARENT_DIR = os.path.dirname(_APP_DIR)                  # LnTCamp 2026/
_DB_NAME = "superstore (1).sqlite"
# Cari di streamlit_app/ dulu, lalu di parent
if os.path.exists(os.path.join(_APP_DIR, _DB_NAME)):
    DB_PATH = os.path.join(_APP_DIR, _DB_NAME)
else:
    DB_PATH = os.path.join(_PARENT_DIR, _DB_NAME)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql: str, params=()) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn, params=params)
    finally:
        conn.close()
    return df


# ─── KPI ────────────────────────────────────────────────────────────────────

def get_kpi():
    sql = """
        SELECT
            ROUND(SUM(oi.sales), 2)          AS total_revenue,
            COUNT(DISTINCT o.order_key)       AS total_orders,
            ROUND(SUM(oi.profit), 2)          AS total_profit,
            ROUND(AVG(oi.discount) * 100, 1)  AS avg_discount_pct,
            COUNT(DISTINCT o.customer_id)     AS total_customers,
            ROUND(SUM(oi.profit) / SUM(oi.sales) * 100, 1) AS profit_margin_pct
        FROM order_items oi
        JOIN orders o ON oi.order_key = o.order_key
    """
    return query(sql).iloc[0]


# ─── CHARTS ─────────────────────────────────────────────────────────────────

def get_revenue_by_year():
    sql = """
        SELECT oi.year, 
               ROUND(SUM(oi.sales), 2) AS revenue,
               ROUND(SUM(oi.profit), 2) AS profit
        FROM order_items oi
        GROUP BY oi.year
        ORDER BY oi.year
    """
    return query(sql)


def get_sales_by_category():
    sql = """
        SELECT p.category, 
               ROUND(SUM(oi.sales), 2) AS sales
        FROM order_items oi
        JOIN dim_products p ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY sales DESC
    """
    return query(sql)


def get_profit_by_market():
    sql = """
        SELECT l.market,
               ROUND(SUM(oi.profit), 2) AS profit,
               ROUND(SUM(oi.sales), 2)  AS sales
        FROM order_items oi
        JOIN orders o ON oi.order_key = o.order_key
        JOIN dim_locations l ON o.location_id = l.location_id
        GROUP BY l.market
        ORDER BY profit DESC
    """
    return query(sql)


def get_top_subcategory():
    sql = """
        SELECT p.sub_category,
               p.category,
               ROUND(SUM(oi.sales), 2)   AS sales,
               ROUND(SUM(oi.profit), 2)  AS profit
        FROM order_items oi
        JOIN dim_products p ON oi.product_id = p.product_id
        GROUP BY p.sub_category, p.category
        ORDER BY sales DESC
        LIMIT 10
    """
    return query(sql)


def get_orders_by_shipmode():
    sql = """
        SELECT o.ship_mode,
               COUNT(DISTINCT o.order_key) AS order_count
        FROM orders o
        GROUP BY o.ship_mode
        ORDER BY order_count DESC
    """
    return query(sql)


def get_monthly_trend():
    sql = """
        SELECT oi.year,
               oi.week_num,
               ROUND(SUM(oi.sales), 2)   AS sales,
               ROUND(SUM(oi.profit), 2)  AS profit
        FROM order_items oi
        GROUP BY oi.year, oi.week_num
        ORDER BY oi.year, oi.week_num
    """
    return query(sql)


def get_profit_vs_discount():
    sql = """
        SELECT oi.discount * 100 AS discount_pct,
               oi.profit,
               p.category
        FROM order_items oi
        JOIN dim_products p ON oi.product_id = p.product_id
        WHERE oi.sales > 0
        LIMIT 5000
    """
    return query(sql)


def get_profit_distribution():
    sql = """
        SELECT oi.profit,
               p.category
        FROM order_items oi
        JOIN dim_products p ON oi.product_id = p.product_id
        LIMIT 10000
    """
    return query(sql)


def get_sales_by_region():
    sql = """
        SELECT l.region,
               l.market,
               ROUND(SUM(oi.sales), 2)   AS sales,
               ROUND(SUM(oi.profit), 2)  AS profit,
               COUNT(DISTINCT o.order_key) AS orders
        FROM order_items oi
        JOIN orders o ON oi.order_key = o.order_key
        JOIN dim_locations l ON o.location_id = l.location_id
        GROUP BY l.region, l.market
        ORDER BY sales DESC
    """
    return query(sql)


def get_segment_stats():
    sql = """
        SELECT c.segment,
               ROUND(SUM(oi.sales), 2)            AS sales,
               ROUND(SUM(oi.profit), 2)           AS profit,
               COUNT(DISTINCT o.customer_id)      AS customers,
               COUNT(DISTINCT o.order_key)        AS orders
        FROM order_items oi
        JOIN orders o ON oi.order_key = o.order_key
        JOIN dim_customers c ON o.customer_id = c.customer_id
        GROUP BY c.segment
    """
    return query(sql)


def get_priority_stats():
    sql = """
        SELECT o.order_priority,
               COUNT(DISTINCT o.order_key)  AS orders,
               ROUND(SUM(oi.sales), 2)      AS sales,
               ROUND(SUM(oi.profit), 2)     AS profit
        FROM orders o
        JOIN order_items oi ON o.order_key = oi.order_key
        GROUP BY o.order_priority
        ORDER BY orders DESC
    """
    return query(sql)


# ─── DATA EXPLORER ──────────────────────────────────────────────────────────

def get_orders_table(search="", category="", market="", limit=500):
    where_clauses = []
    params = []

    if search:
        where_clauses.append(
            "(o.order_id_raw LIKE ? OR c.customer_name LIKE ? OR p.product_name LIKE ?)"
        )
        like = f"%{search}%"
        params += [like, like, like]

    if category and category != "All":
        where_clauses.append("p.category = ?")
        params.append(category)

    if market and market != "All":
        where_clauses.append("l.market = ?")
        params.append(market)

    where = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    sql = f"""
        SELECT
            o.order_id_raw          AS "Order ID",
            c.customer_name         AS "Customer",
            c.segment               AS "Segment",
            p.category              AS "Category",
            p.sub_category          AS "Sub-Category",
            ROUND(oi.sales, 2)      AS "Sales (USD)",
            ROUND(oi.profit, 2)     AS "Profit (USD)",
            ROUND(oi.discount*100,1) AS "Discount (%)",
            oi.quantity             AS "Qty",
            ROUND(oi.shipping_cost,2) AS "Ship Cost",
            o.ship_mode             AS "Ship Mode",
            o.order_priority        AS "Priority",
            l.market                AS "Market",
            l.region                AS "Region",
            o.order_date            AS "Order Date"
        FROM order_items oi
        JOIN orders o       ON oi.order_key = o.order_key
        JOIN dim_customers c ON o.customer_id = c.customer_id
        JOIN dim_products p  ON oi.product_id = p.product_id
        JOIN dim_locations l ON o.location_id = l.location_id
        {where}
        ORDER BY o.order_date DESC
        LIMIT ?
    """
    params.append(limit)
    return query(sql, tuple(params))


def get_customers_table(search=""):
    where = ""
    params = []
    if search:
        where = "WHERE customer_name LIKE ? OR segment LIKE ?"
        params = [f"%{search}%", f"%{search}%"]
    sql = f"""
        SELECT customer_id AS "Customer ID",
               customer_name AS "Customer Name",
               segment AS "Segment"
        FROM dim_customers
        {where}
        ORDER BY customer_name
        LIMIT 1000
    """
    return query(sql, tuple(params))


def get_products_table(search="", category=""):
    where_clauses = []
    params = []
    if search:
        where_clauses.append("(product_name LIKE ? OR sub_category LIKE ?)")
        params += [f"%{search}%", f"%{search}%"]
    if category and category != "All":
        where_clauses.append("category = ?")
        params.append(category)
    where = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    sql = f"""
        SELECT product_id AS "Product ID",
               category AS "Category",
               sub_category AS "Sub-Category",
               product_name AS "Product Name"
        FROM dim_products
        {where}
        ORDER BY category, sub_category, product_name
        LIMIT 1000
    """
    return query(sql, tuple(params))


def get_locations_table(search="", market=""):
    where_clauses = []
    params = []
    if search:
        where_clauses.append("(city LIKE ? OR country LIKE ? OR state LIKE ?)")
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if market and market != "All":
        where_clauses.append("market = ?")
        params.append(market)
    where = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    sql = f"""
        SELECT city AS "City", state AS "State", country AS "Country",
               region AS "Region", market AS "Market"
        FROM dim_locations
        {where}
        ORDER BY market, country, city
        LIMIT 1000
    """
    return query(sql, tuple(params))


def get_distinct_values(table, column):
    sql = f"SELECT DISTINCT {column} FROM {table} ORDER BY {column}"
    df = query(sql)
    return df[column].tolist()
