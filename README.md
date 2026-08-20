# 🫀 CardioAI - Heart Disease Risk Assessment & Analytics

CardioAI is an end-to-end Machine Learning web application designed to predict heart disease risk based on clinical health parameters, blood biomarkers, and lifestyle factors. It delivers real-time risk assessment, probability breakdown, and personalized clinical recommendations.

🚀 **Live Demo:** [https://cardioai-8zcb.onrender.com/](https://cardioai-8zcb.onrender.com/)

---

## ✨ Features

- **Interactive Clinical Form:** Input patient demographics, vitals (Blood Pressure, Heart Rate), lipid panel (Cholesterol, LDL, HDL, Triglycerides), and lifestyle indicators.
- **Real-Time ML Inference:** Instant prediction of heart disease risk percentage using trained machine learning models.
- **Personalized Recommendations:** Dynamic actionable advice tailored to individual risk factors (e.g. glycemic control, lipid management, physical activity).
- **Responsive UI:** Modern, clean interface optimized for desktop and mobile devices.

---

## 🛠️ Tech Stack

- **Machine Learning & Data Processing:** Python, Scikit-Learn, Pandas, NumPy
- **Backend Framework:** Flask, Gunicorn
- **Frontend:** HTML5, Modern CSS3, JavaScript (Fetch API)
- **Deployment:** Render

---

## 📁 Project Structure

```text
cardioai/
├── app.py                            # Flask backend API & recommendation engine
├── heart_disease_risk_2026.csv       # Dataset used for model training & evaluation
├── heart_disease_risk_analysis.ipynb # Jupyter notebook for EDA & ML pipeline
├── model.pkl                         # Serialized trained machine learning model
├── requirements.txt                  # Python dependencies
├── Procfile                          # Deployment start command for Heroku/Render
├── render.yaml                       # Render blueprint specification
├── static/
│   ├── css/style.css                 # Custom CSS styling
│   └── js/main.js                    # Interactive form handler & API calls
└── templates/
    └── index.html                    # Main web UI template
```

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/praveshgrewal/cardioai.git
   cd cardioai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```

5. **Open in Browser:**
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## 🌐 Deployment

The application is deployed on Render using Gunicorn.
- **Start Command:** `gunicorn app:app`
- **Build Command:** `pip install -r requirements.txt`
