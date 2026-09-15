# StoreIQ Admin — Global Superstore Analytics

Sistem Admin Dashboard lengkap dengan integrasi AI Predictor berbasis Streamlit.

## 🚀 Fitur Utama
1. **Dashboard Analytics**: KPI, tren pendapatan, profitabilitas market, performa kategori (Chart.js via Plotly).
2. **Data Explorer**: Modul Orders, Products, Customers, dan Locations dengan pencarian dan filter.
3. **AI Predictor (XGBoost)**: 
   - **Klasifikasi**: Prediksi status (PROFIT / LOSS) dan tingkat keyakinan (confidence).
   - **Regresi**: Estimasi nilai margin profit dalam USD berdasarkan parameter yang di-input.
   - **What-If Analysis**: Simulasi perubahan diskon terhadap profit margin.

## 🛠️ Stack & Struktur
- **Frontend / Framework**: [Streamlit](https://streamlit.io/) + Custom CSS
- **Visualization**: Plotly Graph Objects & Express
- **Database**: SQLite (`superstore (1).sqlite`)
- **Machine Learning**: `scikit-learn` & `xgboost` (Model pre-trained dalam `model_klasifikasi/` & `model_regresi/`)

```text
streamlit_app/
├── app.py                         # Main entry point (Streamlit Home)
├── requirements.txt               # Dependencies
├── superstore (1).sqlite          # Database (dikopi ke dalam folder untuk deployment)
├── utils/
│   ├── db.py                      # Logic interaksi SQLite (KPI, queries, tables)
│   └── model.py                   # Preprocessing form input & load model XGBoost
├── pages/
│   ├── 01_📊_Dashboard.py
│   ├── 02_📦_Orders.py
│   ├── 03_🛒_Products.py
│   ├── 04_👥_Customers.py
│   ├── 05_🌍_Locations.py
│   └── 06_🤖_AI_Predictor.py
├── model_klasifikasi/             # XGBoost & Scaler
└── model_regresi/                 # XGBoost & Scaler
```

## 💻 Menjalankan secara Lokal

1. Buka terminal dan masuk ke folder `streamlit_app`.
2. Install semua dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Buka browser pada [http://localhost:8501](http://localhost:8501)

## 🌐 Deploy ke Streamlit Community Cloud

Aplikasi ini sudah dipersiapkan struktur direktori dan dependencies-nya untuk langsung berjalan di **Streamlit Community Cloud**.

1. **Commit & Push** folder `streamlit_app/` (termasuk db `.sqlite` dan `model_*.pkl`) ke GitHub repository.
2. Login ke [share.streamlit.io](https://share.streamlit.io).
3. Klik **New app**.
4. Pilih repository GitHub Anda.
5. Pada bagian **Main file path**, isi dengan:
   `streamlit_app/app.py`
6. Klik **Deploy**.

> **Catatan:** Model XGBoost ini di-generate pada versi *scikit-learn/xgboost* tertentu. Jika di kemudian hari muncul warning kompatibilitas versi saat load `.pkl`, Anda dapat menjalankan ulang skrip pembentukan scaler atau retrain sesuai env saat deployment. File `rebuild_scalers.py` disediakan untuk rebuild `StandardScaler` jika terjadi `UnpicklingError` pada scaler.
