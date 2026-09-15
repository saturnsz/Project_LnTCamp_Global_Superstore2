# Global Superstore Admin Dashboard — Implementation Plan

## Overview

Sistem admin dashboard **private** berbasis web untuk Global Superstore Dataset. Terdiri dari dua bagian utama:
1. **Dashboard Data** — Analytics & visualisasi data dari SQLite
2. **AI Page** — Dua tool prediksi: Klasifikasi (Profit/Loss) dan Regresi (Estimasi Profit USD)

Backend: **Flask (Python)** — melayani API data dari SQLite + inferensi model ML  
Frontend: **Pure HTML/CSS/JS** — dark theme ala CRM panel referensi (hitam, aksen biru/ungu, glassmorphism)

---

## Arsitektur

```
project LnTCamp/
├── app.py                  # Flask backend (API endpoints)
├── templates/
│   └── index.html          # Single-page app (SPA)
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── dashboard.js    # Chart.js visualisasi data
│       └── ai.js           # Form AI + fetch prediksi
├── model klasfikasi/       # (existing)
├── model regresii/         # (existing)
└── superstore (1).sqlite   # (existing)
```

---

## Pages / Sections

### 1. Sidebar Navigation
- Logo "StoreIQ Admin"
- Menu: Dashboard, Orders, Products, Customers, Locations, AI Predictor
- Active state indicator
- Collapse mode

### 2. Dashboard Page (Home)
KPI Cards:
- Total Revenue (SUM sales)
- Total Orders (COUNT orders)
- Total Profit (SUM profit)
- Avg Discount (AVG discount)

Charts (Chart.js):
- Revenue by Year (Bar chart)
- Sales by Category (Donut chart)
- Profit by Market (Horizontal bar)
- Top 10 Sub-Categories (Bar)
- Orders by Ship Mode (Pie)
- Monthly sales trend (Line chart)

### 3. Orders Page
- Table order_items JOIN orders dengan pagination, search, filter
- Kolom: Order ID, Customer, Category, Sales, Profit, Discount, Ship Mode, Priority, Date, Status

### 4. Products Page
- Table dim_products dengan pagination & search
- Stats: total products by category

### 5. Customers Page
- Table dim_customers dengan pagination & search
- Stats: segmentasi customer

### 6. Locations Page
- Table dim_locations dengan pagination & search
- Stats: per market & region

### 7. AI Predictor Page (Terpisah/Tab)
Dua sub-tab:
- **🔍 Detektor Status (Klasifikasi)** — Prediksi Profit/Loss
- **📈 Estimasi Profit (Regresi)** — Estimasi nilai profit USD

Input form (11 parameter dari PRD):
- Sales_USD, Diskon_Persen, Biaya_Kirim_USD, Kuantitas
- Kategori, Sub_Kategori, Segment, Market, Ship_Mode, Order_Priority, Region

Output:
- Klasifikasi: Badge PROFIT ✅ / LOSS ❌ + confidence %
- Regresi: Estimasi nominal USD + indikator status

---

## Backend API Endpoints (Flask)

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serve index.html |
| `/api/kpi` | GET | KPI summary stats |
| `/api/revenue-by-year` | GET | Revenue per tahun |
| `/api/sales-by-category` | GET | Sales per category |
| `/api/profit-by-market` | GET | Profit per market |
| `/api/top-subcategory` | GET | Top sub-categories |
| `/api/orders-by-shipmode` | GET | Orders per ship mode |
| `/api/monthly-trend` | GET | Monthly sales trend |
| `/api/orders` | GET | Paginated orders (q, page, limit) |
| `/api/products` | GET | Paginated products |
| `/api/customers` | GET | Paginated customers |
| `/api/locations` | GET | Paginated locations |
| `/api/predict/classify` | POST | XGBoost klasifikasi |
| `/api/predict/regress` | POST | XGBoost regresi |

---

## Design System (referensi CRM panel)

- Background: `#0f0f14` (near-black)
- Cards: `#1a1a24` dengan `border: 1px solid rgba(255,255,255,0.06)`
- Accent Blue: `#4f8ef7`
- Accent Purple: `#8b5cf6`
- Accent Green: `#22c55e`
- Accent Red: `#ef4444`
- Accent Yellow/Orange: `#f59e0b`
- Font: Inter (Google Fonts)
- Glassmorphism cards, smooth transitions, hover effects

---

## Verification Plan

1. Start Flask server: `python app.py`
2. Open browser: `http://localhost:5000`
3. Test semua dashboard chart tampil data benar
4. Test tabel pagination & search
5. Test AI form klasifikasi → output PROFIT/LOSS
6. Test AI form regresi → output estimasi USD
