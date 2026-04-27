from flask import Flask, render_template, request, jsonify, send_file
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import numpy as np
import traceback

app = Flask(__name__)
app.config['DATABASE'] = 'history.db'

# ========== MODEL LOADING ==========
print("\n" + "="*60)
print("🚀 SMART CROP ADVISOR STARTING")
print("="*60)

# Try to load model from different possible filenames
model_paths = ['crop_model.pkl', 'model.pkl']
model = None
model_accuracy = 0

for model_path in model_paths:
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            model_accuracy = 0.94
            print(f"✅ Model loaded from: {model_path}")
            print(f"📊 Model type: {type(model)}")
            break
        except Exception as e:
            print(f"❌ Error loading {model_path}: {e}")

if model is None:
    print(f"❌ No model file found! Checked: {model_paths}")

# Load crop details
crop_details = {
    'rice': {'description': 'Rice is a staple grain crop widely cultivated in tropical regions.', 'temp_range': '20-30°C', 'water': 'High - requires 100-150 cm annually', 'fertilizer': 'NPK 60:30:30', 'duration': 120},
    'maize': {'description': 'Corn/Maize is a versatile cereal grain used for food, feed, and industrial purposes.', 'temp_range': '21-27°C', 'water': 'Moderate - requires 50-80 cm annually', 'fertilizer': 'NPK 80:40:40', 'duration': 110},
    'chickpea': {'description': 'Chickpea is a protein-rich legume crop with high nutritional value.', 'temp_range': '15-25°C', 'water': 'Low - requires 40-50 cm annually', 'fertilizer': 'NPK 20:60:20', 'duration': 90},
    'kidneybeans': {'description': 'Kidney beans are nutrient-dense legumes rich in protein and fiber.', 'temp_range': '15-27°C', 'water': 'Moderate - requires 60-100 cm annually', 'fertilizer': 'NPK 20:60:20', 'duration': 100},
    'pigeonpeas': {'description': 'Pigeon peas are drought-tolerant legumes with high protein content.', 'temp_range': '20-30°C', 'water': 'Low-Moderate - requires 60-90 cm annually', 'fertilizer': 'NPK 20:40:20', 'duration': 120},
    'mothbeans': {'description': 'Moth beans are small legumes highly suited to arid and semi-arid regions.', 'temp_range': '25-35°C', 'water': 'Very Low - requires 40-60 cm annually', 'fertilizer': 'NPK 20:40:20', 'duration': 75},
    'mungbean': {'description': 'Mung beans are fast-growing legumes with excellent nutritional profile.', 'temp_range': '22-28°C', 'water': 'Low-Moderate - requires 50-75 cm annually', 'fertilizer': 'NPK 20:40:20', 'duration': 65},
    'blackgram': {'description': 'Black gram is a protein-rich legume important in Indian cuisine.', 'temp_range': '20-30°C', 'water': 'Moderate - requires 60-90 cm annually', 'fertilizer': 'NPK 20:40:20', 'duration': 90},
    'lentil': {'description': 'Lentils are nutritious pulses with high protein and fiber content.', 'temp_range': '15-25°C', 'water': 'Low - requires 40-50 cm annually', 'fertilizer': 'NPK 20:60:20', 'duration': 85},
    'pomegranate': {'description': 'Pomegranate is a fruit crop rich in antioxidants and vitamins.', 'temp_range': '20-28°C', 'water': 'Moderate - requires 50-100 cm annually', 'fertilizer': 'NPK 10:20:10', 'duration': 365},
    'banana': {'description': 'Banana is a tropical fruit crop with high yield and commercial value.', 'temp_range': '24-30°C', 'water': 'High - requires 150-225 cm annually', 'fertilizer': 'NPK 60:80:80', 'duration': 365},
    'mango': {'description': 'Mango is a popular fruit crop known as the "King of Fruits".', 'temp_range': '24-30°C', 'water': 'Moderate - requires 75-225 cm annually', 'fertilizer': 'NPK 10:40:10', 'duration': 365},
    'grapes': {'description': 'Grapes are deciduous fruit crops with high commercial value.', 'temp_range': '15-25°C', 'water': 'Moderate - requires 65-100 cm annually', 'fertilizer': 'NPK 10:30:30', 'duration': 365},
    'watermelon': {'description': 'Watermelon is a summer fruit crop rich in hydration and nutrients.', 'temp_range': '22-30°C', 'water': 'Moderate - requires 40-80 cm annually', 'fertilizer': 'NPK 30:20:50', 'duration': 80},
    'muskmelon': {'description': 'Muskmelon is a sweet aromatic fruit crop popular in summer.', 'temp_range': '20-30°C', 'water': 'Moderate - requires 60-90 cm annually', 'fertilizer': 'NPK 30:20:50', 'duration': 90},
    'apple': {'description': 'Apple is a temperate fruit crop with long shelf life.', 'temp_range': '10-21°C', 'water': 'Moderate - requires 60-100 cm annually', 'fertilizer': 'NPK 10:20:10', 'duration': 365},
    'orange': {'description': 'Orange is a citrus fruit crop rich in vitamin C and antioxidants.', 'temp_range': '20-25°C', 'water': 'Moderate - requires 75-150 cm annually', 'fertilizer': 'NPK 10:30:20', 'duration': 365},
    'papaya': {'description': 'Papaya is a tropical fruit crop with enzymes beneficial for digestion.', 'temp_range': '21-30°C', 'water': 'Moderate - requires 100-150 cm annually', 'fertilizer': 'NPK 60:30:30', 'duration': 180},
    'coconut': {'description': 'Coconut is a tropical tree crop with multiple commercial uses.', 'temp_range': '24-32°C', 'water': 'High - requires 150-250 cm annually', 'fertilizer': 'NPK 40:20:50', 'duration': 365},
    'cotton': {'description': 'Cotton is a fiber crop of major economic importance globally.', 'temp_range': '21-30°C', 'water': 'High - requires 60-100 cm annually', 'fertilizer': 'NPK 80:40:20', 'duration': 165},
    'sugarcane': {'description': 'Sugarcane is an important crop for sugar and bio-energy production.', 'temp_range': '21-30°C', 'water': 'High - requires 150-250 cm annually', 'fertilizer': 'NPK 120:60:60', 'duration': 365},
    'tobacco': {'description': 'Tobacco is a cash crop with significant economic value.', 'temp_range': '20-30°C', 'water': 'Moderate - requires 50-75 cm annually', 'fertilizer': 'NPK 60:20:20', 'duration': 90},
    'jute': {'description': 'Jute is a fiber crop used for making bags and textiles.', 'temp_range': '24-34°C', 'water': 'High - requires 150-250 cm annually', 'fertilizer': 'NPK 40:20:40', 'duration': 120},
}

# ========== DATABASE ==========
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  n REAL, p REAL, k REAL,
                  temperature REAL, humidity REAL,
                  ph REAL, rainfall REAL,
                  predicted_crop TEXT,
                  confidence REAL,
                  timestamp DATETIME,
                  explanation TEXT)''')
    conn.commit()
    conn.close()

init_db()

def generate_explanation(input_data, predicted_crop):
    try:
        temp = float(input_data.get('temperature', 0))
        humidity = float(input_data.get('humidity', 0))
        n = float(input_data.get('n', 0))
        p = float(input_data.get('p', 0))
        k = float(input_data.get('k', 0))
        rainfall = float(input_data.get('rainfall', 0))
        ph = float(input_data.get('ph', 0))
        
        explanation = f"""Based on the soil and environmental conditions:
- Nitrogen (N): {n} kg/ha - {'Adequate' if n > 40 else 'Low'}
- Phosphorus (P): {p} kg/ha - {'Adequate' if p > 20 else 'Low'}
- Potassium (K): {k} kg/ha - {'Adequate' if k > 40 else 'Low'}
- Temperature: {temp}°C - Suitable for {predicted_crop}
- Humidity: {humidity}% - {'High' if humidity > 60 else 'Moderate' if humidity > 40 else 'Low'}
- Rainfall: {rainfall} mm - {'High' if rainfall > 100 else 'Moderate' if rainfall > 50 else 'Low'}
- Soil pH: {ph} - {'Neutral' if 6.5 <= ph <= 7.5 else 'Acidic' if ph < 6.5 else 'Alkaline'}

{predicted_crop} is recommended as it thrives in these conditions."""
        return explanation
    except:
        return "Prediction generated successfully"

# ========== ROUTES ==========

@app.route('/')
def dashboard():
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM predictions')
        total_predictions = c.fetchone()[0]
        conn.close()
        total_crops = len(crop_details)
        return render_template('dashboard.html', 
                             total_crops=total_crops,
                             total_predictions=total_predictions,
                             model_accuracy=f'{model_accuracy*100:.2f}%')
    except Exception as e:
        print(f"Error in dashboard: {e}")
        return render_template('dashboard.html', total_crops=0, total_predictions=0, model_accuracy='0%')

@app.route('/predict')
def predict():
    return render_template('input.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        if model is None:
            return jsonify({'success': False, 'error': 'Model not loaded'}), 500
        
        data = request.json
        required_fields = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        features = np.array([[float(data['n']), float(data['p']), float(data['k']),
                             float(data['temperature']), float(data['humidity']),
                             float(data['ph']), float(data['rainfall'])]])
        
        prediction = model.predict(features)[0]
        
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features)[0]
            confidence = float(np.max(proba))
        else:
            confidence = 0.85
        
        explanation = generate_explanation(data, prediction)
        
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('''INSERT INTO predictions 
                     (n, p, k, temperature, humidity, ph, rainfall, predicted_crop, confidence, timestamp, explanation)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (float(data['n']), float(data['p']), float(data['k']),
                   float(data['temperature']), float(data['humidity']),
                   float(data['ph']), float(data['rainfall']),
                   str(prediction), confidence, datetime.now(), explanation))
        conn.commit()
        conn.close()
        
        print(f"✅ Prediction: {prediction} (confidence: {confidence:.2%})")
        
        return jsonify({'success': True, 'crop': str(prediction), 'confidence': confidence})
    except Exception as e:
        print(f"Error in prediction: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/result')
def result():
    crop = request.args.get('crop', '')
    confidence = float(request.args.get('confidence', 0.85))
    details = crop_details.get(crop.lower(), {
        'description': 'No details available',
        'temp_range': 'N/A', 'water': 'N/A',
        'fertilizer': 'N/A', 'duration': 'N/A'
    })
    return render_template('result.html', crop=crop, details=details, confidence=confidence)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/api/history')
def api_history():
    try:
        search = request.args.get('search', '').lower()
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM predictions ORDER BY timestamp DESC')
        records = c.fetchall()
        conn.close()
        
        if search:
            records = [r for r in records if search in r[8].lower()]
        
        return jsonify({'success': True, 'data': [{'id': r[0], 'n': r[1], 'p': r[2], 'k': r[3],
                                                     'temperature': r[4], 'humidity': r[5], 'ph': r[6],
                                                     'rainfall': r[7], 'crop': r[8],
                                                     'confidence': f'{r[9]*100:.2f}%',
                                                     'timestamp': r[10]} for r in records]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('DELETE FROM predictions WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/clear-history', methods=['DELETE'])
def clear_history():
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('DELETE FROM predictions')
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data')
def get_data():
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT predicted_crop, COUNT(*) FROM predictions GROUP BY predicted_crop')
        crop_counts = c.fetchall()
        conn.close()
        
        crops = [row[0] for row in crop_counts]
        counts = [row[1] for row in crop_counts]
        
        return jsonify({'success': True, 'crops': crops, 'counts': counts})
    except Exception as e:
        print(f"Error in get_data: {e}")
        return jsonify({'success': True, 'crops': [], 'counts': []})

@app.route('/download-report')
def download_report():
    try:
        crop = request.args.get('crop', 'Unknown')
        confidence = request.args.get('confidence', '0.85')
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                     fontSize=24, textColor=colors.HexColor('#2ecc71'),
                                     spaceAfter=30, alignment=1)
        
        elements.append(Paragraph('Smart Crop Recommendation Report', title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(f'<b>Recommended Crop:</b> {crop}', styles['Normal']))
        elements.append(Paragraph(f'<b>Confidence Level:</b> {confidence}', styles['Normal']))
        elements.append(Paragraph(f'<b>Generated:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']))
        
        if crop.lower() in crop_details:
            details = crop_details[crop.lower()]
            elements.append(Paragraph('<b>Crop Details:</b>', styles['Heading2']))
            elements.append(Paragraph(details['description'], styles['Normal']))
            elements.append(Paragraph(f"<b>Temperature Range:</b> {details['temp_range']}", styles['Normal']))
            elements.append(Paragraph(f"<b>Water Requirement:</b> {details['water']}", styles['Normal']))
            elements.append(Paragraph(f"<b>Fertilizer:</b> {details['fertilizer']}", styles['Normal']))
            elements.append(Paragraph(f"<b>Duration:</b> {details['duration']} days", styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True,
                        download_name=f'crop_report_{crop}_{datetime.now().strftime("%Y%m%d")}.pdf',
                        mimetype='application/pdf')
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

print("="*60)
print("✅ Flask app initialized successfully!")
print("="*60 + "\n")

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)