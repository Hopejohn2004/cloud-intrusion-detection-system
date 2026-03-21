"""
Train XGBoost model on CIC-IDS2017 dataset
Run this once to generate the model file: model/intrusion_model.pkl
Dataset: https://www.unb.ca/cic/datasets/ids-2017.html
"""

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import glob

# ── CONFIG ──────────────────────────────────────────────────────────────────
DATASET_PATH = "dataset/"   # Folder containing CIC-IDS2017 CSV files
MODEL_DIR    = "model/"
MODEL_FILE   = os.path.join(MODEL_DIR, "intrusion_model.pkl")
ENCODER_FILE = os.path.join(MODEL_DIR, "label_encoder.pkl")
# ────────────────────────────────────────────────────────────────────────────

os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 60)
print("  Cloud Intrusion Detection — Model Training")
print("=" * 60)

# Load dataset
csv_files = glob.glob(os.path.join(DATASET_PATH, "*.csv"))
if not csv_files:
    print(f"\n❌  No CSV files found in '{DATASET_PATH}'")
    print("    Download the CIC-IDS2017 dataset and place CSVs there.")
    print("    URL: https://www.unb.ca/cic/datasets/ids-2017.html\n")
    exit(1)

print(f"\n📂  Found {len(csv_files)} CSV file(s). Loading...")
dfs = []
for f in csv_files:
    df_tmp = pd.read_csv(f, low_memory=False)
    df_tmp.columns = df_tmp.columns.str.strip()
    dfs.append(df_tmp)
    print(f"    ✅  {os.path.basename(f)} — {len(df_tmp):,} rows")

df = pd.concat(dfs, ignore_index=True)
print(f"\n📊  Total rows: {len(df):,}")
print(f"    Columns: {len(df.columns)}")

# Clean
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)
print(f"    After cleaning: {len(df):,} rows")

# Label
label_col = "Label"
print(f"\n🏷️   Class distribution:\n{df[label_col].value_counts()}")

le = LabelEncoder()
y = le.fit_transform(df[label_col])
X = df.drop(columns=[label_col]).select_dtypes(include=[np.number])

print(f"\n🔢  Features used: {X.shape[1]}")
print(f"    Classes: {list(le.classes_)}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n✂️   Train: {len(X_train):,} | Test: {len(X_test):,}")

# Train
print("\n🚀  Training XGBoost model...")
model = XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="mlogloss",
    tree_method="hist",
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=50)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n✅  Accuracy: {acc * 100:.4f}%")
print("\n📋  Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save
joblib.dump(model, MODEL_FILE)
joblib.dump(le,    ENCODER_FILE)
print(f"\n💾  Model saved  → {MODEL_FILE}")
print(f"💾  Encoder saved → {ENCODER_FILE}")
print("\n🎉  Training complete! Run 'python app.py' to start the dashboard.")
