import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load serialized model pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
model_artifact = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_artifact = pickle.load(f)
        print(f"✅ Loaded model pipeline successfully! Model: {model_artifact.get('model_name', 'Trained Classifier')}")
    else:
        print("⚠️ Warning: model.pkl not found! Run pipeline first.")
except Exception as e:
    print(f"❌ Error loading model.pkl: {str(e)}")


def generate_recommendations(data, risk_score):
    """Generate personalized clinical and lifestyle recommendations based on patient data."""
    recommendations = []
    
    # Blood Pressure check
    if data['resting_bp_systolic'] >= 130 or data['resting_bp_diastolic'] >= 85:
        recommendations.append({
            'icon': '🫀',
            'title': 'Manage Blood Pressure',
            'desc': f"Systolic ({data['resting_bp_systolic']} mmHg) or Diastolic ({data['resting_bp_diastolic']} mmHg) is elevated. Reduce sodium intake and consult a physician."
        })

    # Cholesterol check
    if data['cholesterol_total'] > 200 or data['ldl'] > 130:
        recommendations.append({
            'icon': '🩸',
            'title': 'Lipid Management',
            'desc': f"Total cholesterol ({data['cholesterol_total']} mg/dL) or LDL ({data['ldl']} mg/dL) is high. Incorporate soluble fiber and healthy omega-3 fatty acids."
        })

    # Glucose / HbA1c check
    if data['hba1c'] >= 5.7 or data['fasting_blood_sugar'] >= 100:
        recommendations.append({
            'icon': '📊',
            'title': 'Glycemic Control',
            'desc': f"HbA1c ({data['hba1c']}%) indicates elevated blood sugar level. Monitor refined carbohydrate intake."
        })

    # Exercise check
    if data['exercise_minutes_per_week'] < 150:
        recommendations.append({
            'icon': '🏃',
            'title': 'Increase Exercise',
            'desc': f"Current weekly exercise ({data['exercise_minutes_per_week']} mins) is below the recommended 150 mins/week of moderate aerobic activity."
        })

    # Smoking check
    if data['smoker_status'] in ['Current']:
        recommendations.append({
            'icon': '🚭',
            'title': 'Smoking Cessation',
            'desc': "Smoking significantly increases cardiovascular disease risk. Seek cessation support program."
        })

    # Stress check
    if data['stress_score'] > 50:
        recommendations.append({
            'icon': '🧘',
            'title': 'Stress Reduction',
            'desc': f"Stress score ({data['stress_score']}/100) is elevated. Practice mindfulness, meditation, or structured relaxation."
        })

    if not recommendations:
        recommendations.append({
            'icon': '🌟',
            'title': 'Maintain Healthy Lifestyle',
            'desc': "Your clinical markers are currently in optimal ranges. Continue regular health screenings and balanced diet."
        })

    return recommendations


@app.route('/')
def home():
    """Render main web application interface."""
    model_name = model_artifact.get('model_name', 'Machine Learning Classifier') if model_artifact else "Model Unavailable"
    benchmark_metrics = model_artifact.get('benchmark_metrics', []) if model_artifact else []
    return render_template('index.html', model_name=model_name, metrics=benchmark_metrics)


@app.route('/api/predict', methods=['POST'])
def predict_api():
    """API Endpoint returning JSON prediction, risk level, and recommendations."""
    if not model_artifact or 'pipeline' not in model_artifact:
        return jsonify({'error': 'Model pickle file (model.pkl) is not loaded or missing!'}), 500

    try:
        req_data = request.get_json(force=True)
        
        # Parse inputs with type casting and fallbacks
        patient_data = {
            'age': int(req_data.get('age', 50)),
            'sex': str(req_data.get('sex', 'Male')),
            'resting_bp_systolic': int(req_data.get('resting_bp_systolic', 120)),
            'resting_bp_diastolic': int(req_data.get('resting_bp_diastolic', 80)),
            'cholesterol_total': int(req_data.get('cholesterol_total', 190)),
            'hdl': int(req_data.get('hdl', 50)),
            'ldl': int(req_data.get('ldl', 100)),
            'triglycerides': int(req_data.get('triglycerides', 120)),
            'fasting_blood_sugar': int(req_data.get('fasting_blood_sugar', 95)),
            'hba1c': float(req_data.get('hba1c', 5.2)),
            'bmi': float(req_data.get('bmi', 24.5)),
            'resting_heart_rate': int(req_data.get('resting_heart_rate', 72)),
            'max_heart_rate_achieved': int(req_data.get('max_heart_rate_achieved', 160)),
            'chest_pain_type': str(req_data.get('chest_pain_type', 'Asymptomatic')),
            'exercise_induced_angina': bool(req_data.get('exercise_induced_angina', False)),
            'st_depression': float(req_data.get('st_depression', 0.5)),
            'family_history': bool(req_data.get('family_history', False)),
            'smoker_status': str(req_data.get('smoker_status', 'Never')),
            'alcohol_units_per_week': float(req_data.get('alcohol_units_per_week', 2.0)),
            'exercise_minutes_per_week': int(req_data.get('exercise_minutes_per_week', 120)),
            'sleep_hours': float(req_data.get('sleep_hours', 7.0)),
            'stress_score': float(req_data.get('stress_score', 30.0)),
            'wearable_owner': bool(req_data.get('wearable_owner', True)),
            'daily_steps': int(req_data.get('daily_steps', 7500)),
            'diet_quality_score': float(req_data.get('diet_quality_score', 65.0))
        }

        # Convert to Pandas DataFrame matching feature names
        input_df = pd.DataFrame([patient_data])
        
        # Pipeline prediction
        pipeline = model_artifact['pipeline']
        prediction = int(pipeline.predict(input_df)[0])
        probability = float(pipeline.predict_proba(input_df)[0, 1])
        risk_percentage = round(probability * 100, 1)

        # Classify Risk Level
        if risk_percentage < 30.0:
            risk_level = "Low Risk"
            risk_color = "#10b981" # Green
            badge_class = "badge-success"
        elif risk_percentage < 65.0:
            risk_level = "Moderate Risk"
            risk_color = "#f59e0b" # Orange
            badge_class = "badge-warning"
        else:
            risk_level = "High Risk"
            risk_color = "#ef4444" # Red
            badge_class = "badge-danger"

        recommendations = generate_recommendations(patient_data, risk_percentage)

        return jsonify({
            'success': True,
            'prediction': prediction,
            'probability': probability,
            'risk_percentage': risk_percentage,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'badge_class': badge_class,
            'recommendations': recommendations,
            'model_name': model_artifact.get('model_name', 'ML Classifier')
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/health')
def health():
    """Render deployment health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_artifact is not None
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
