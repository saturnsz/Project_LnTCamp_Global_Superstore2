import sqlite3
import pickle

# Check SQLite schema
conn = sqlite3.connect('superstore (1).sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

for table in tables:
    tname = table[0]
    cursor.execute(f"PRAGMA table_info({tname})")
    cols = cursor.fetchall()
    print(f"\n{tname} columns:")
    for col in cols:
        print(f"  {col}")
    cursor.execute(f"SELECT COUNT(*) FROM {tname}")
    count = cursor.fetchone()
    print(f"  Row count: {count[0]}")

conn.close()

print("\n\n--- Model Klasifikasi Columns ---")
with open('model_klasifikasi/training_columns_clf.pkl', 'rb') as f:
    cols_clf = pickle.load(f)
print("Type:", type(cols_clf))
print("Columns:", cols_clf)

print("\n\n--- Model Regresi Columns ---")
with open('model_regresi/training_columns_reg.pkl', 'rb') as f:
    cols_reg = pickle.load(f)
print("Type:", type(cols_reg))
print("Columns:", cols_reg)
