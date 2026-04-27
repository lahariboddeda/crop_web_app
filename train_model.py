# -*- coding: utf-8 -*-
"""
Crop Recommendation Model Training Script
This script trains and saves the Random Forest model
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import os

print("\n" + "="*60)
print("🌾 CROP RECOMMENDATION MODEL TRAINING")
print("="*60 + "\n")

# ========== STEP 1: LOAD DATASET ==========
print("📥 Loading dataset...")

try:
    df = pd.read_csv('Crop_recommendation.csv')
    print(f"✅ Dataset loaded successfully! Shape: {df.shape}")
except FileNotFoundError:
    print("⚠️ 'Crop_recommendation.csv' not found. Creating dummy dataset...")
    
    # Create a more comprehensive dummy dataset
    np.random.seed(42)
    data = {
        'N': np.random.randint(0, 140, 200),
        'P': np.random.randint(5, 145, 200),
        'K': np.random.randint(5, 205, 200),
        'temperature': np.random.uniform(8, 40, 200),
        'humidity': np.random.uniform(20, 100, 200),
        'ph': np.random.uniform(4.5, 8.5, 200),
        'rainfall': np.random.uniform(20, 350, 200),
        'label': np.random.choice([
            'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
            'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
            'banana', 'mango', 'grapes', 'watermelon', 'muskmelon',
            'apple', 'orange', 'papaya', 'coconut', 'cotton',
            'sugarcane', 'tobacco', 'jute'
        ], 200)
    }
    df = pd.DataFrame(data)
    print(f"✅ Dummy dataset created! Shape: {df.shape}")

# ========== STEP 2: DATA EXPLORATION ==========
print("\n📊 Data Overview:")
print(f"Columns: {list(df.columns)}")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nDataset statistics:")
print(df.describe())

# ========== STEP 3: DATA PREPROCESSING ==========
print("\n🔧 Preprocessing data...")

# Separate features (X) and label (y)
X = df.drop('label', axis=1)  # Features
y = df['label']  # Target

print(f"✅ Features (X) shape: {X.shape}")
print(f"✅ Target (y) shape: {y.shape}")
print(f"✅ Unique crops: {y.unique()}")
print(f"✅ Number of unique crops: {len(y.unique())}")

# ========== STEP 4: TRAIN-TEST SPLIT ==========
print("\n📈 Splitting data into train/test sets (80/20)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

print(f"✅ Training set size: {X_train.shape[0]}")
print(f"✅ Testing set size: {X_test.shape[0]}")

# ========== STEP 5: MODEL TRAINING ==========
print("\n🤖 Training Random Forest Classifier...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("✅ Model trained successfully!")

# ========== STEP 6: MODEL EVALUATION ==========
print("\n📋 Evaluating model...")

# Predictions
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")
print(f"✅ Training Accuracy: {model.score(X_train, y_train) * 100:.2f}%")
print(f"✅ Testing Accuracy: {model.score(X_test, y_test) * 100:.2f}%")

# Feature importance
print(f"\n📊 Feature Importance:")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance)

# ========== STEP 7: SAVE THE MODEL ==========
print("\n💾 Saving model...")

model_filename = 'crop_model.pkl'
joblib.dump(model, model_filename)

# Verify file was saved
if os.path.exists(model_filename):
    file_size = os.path.getsize(model_filename)
    print(f"✅ Model saved successfully as '{model_filename}'")
    print(f"📁 File size: {file_size / 1024:.2f} KB")
    print(f"📁 File path: {os.path.abspath(model_filename)}")
else:
    print(f"❌ Error: Could not save model!")

# ========== STEP 8: TEST THE SAVED MODEL ==========
print("\n🧪 Testing loaded model...")

# Load the model
loaded_model = joblib.load(model_filename)
print(f"✅ Model loaded successfully!")

# Test prediction
test_input = pd.DataFrame([[90, 42, 43, 20.87, 82.00, 6.50, 202.94]],
                          columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

test_prediction = loaded_model.predict(test_input)
test_proba = loaded_model.predict_proba(test_input)

print(f"✅ Test prediction: {test_prediction[0]}")
print(f"✅ Test confidence: {np.max(test_proba[0]) * 100:.2f}%")

print("\n" + "="*60)
print("✅ MODEL TRAINING COMPLETE!")
print("="*60)
print(f"\n✅ The model file 'crop_model.pkl' is ready to use with Flask!")
print(f"✅ Location: {os.path.abspath(model_filename)}")
print(f"✅ Accuracy: {accuracy * 100:.2f}%")
print("\n🚀 Next step: Run your Flask app (python app.py)\n")