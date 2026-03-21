# 🛡️ Cloud Intrusion Detection System

An ML-powered real-time network intrusion detection system built with XGBoost and Flask.

## 🚀 Features
- **99.97% accuracy** on CIC-IDS2017 dataset (2.8M rows)
- Real-time detection of 10+ attack types
- Live dashboard with attack distribution, live feed, and severity scoring
- REST API for predictions

## 🔍 Detected Attack Types
| Attack | Severity | Action |
|--------|----------|--------|
| DDoS | HIGH | BLOCK |
| DoS Hulk | HIGH | BLOCK |
| DoS slowloris | HIGH | BLOCK |
| DoS Slowhttptest | HIGH | BLOCK |
| DoS GoldenEye | HIGH | BLOCK |
| Heartbleed | CRITICAL | BLOCK |
| Bot | HIGH | BLOCK |
| PortScan | MEDIUM | ALERT |
| FTP-Patator | MEDIUM | ALERT |
| SSH-Patator | MEDIUM | ALERT |
| BENIGN | NONE | ALLOW |

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/Hopejohn2004/cloud-intrusion-detection-system.git
cd cloud-intrusion-detection-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Train the model
# Download CIC-IDS2017 dataset → https://www.unb.ca/cic/datasets/ids-2017.html
# Place CSV files in dataset/ folder, then:
python train_model.py

# 4. Run the dashboard
python app.py
```

Then open: http://localhost:5000

## 🗂️ Project Structure
```
cloud-intrusion-detection-system/
├── app.py               ← Flask API + routes
├── train_model.py       ← XGBoost training script
├── requirements.txt
├── README.md
├── dataset/             ← CIC-IDS2017 CSV files (not committed)
├── model/               ← Saved model files (generated after training)
│   ├── intrusion_model.pkl
│   └── label_encoder.pkl
└── templates/
    └── dashboard.html   ← Real-time dashboard UI
```

## 🧠 ML Model
- Algorithm: **XGBoost** (eXtreme Gradient Boosting)
- Dataset: **CIC-IDS2017** (Canadian Institute for Cybersecurity)
- Rows: **2.8 Million** network traffic samples
- Accuracy: **99.97%**
- Features: 78 network flow features

## ☁️ Cloud Deployment (Phase 6)
- AWS EC2 / Render / Railway deployment coming soon

## 👤 Author
Hopejohn2004 — Cloud Engineering
