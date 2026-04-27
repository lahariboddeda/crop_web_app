# 🌾 Smart Crop Recommendation System

An intelligent agriculture platform that recommends the best crop based on soil and environmental conditions using Machine Learning.

## ✨ Features

- **🧠 ML-Based Prediction**: Random Forest model for accurate crop recommendations
- **📊 Data Visualization**: Interactive charts using Chart.js
- **📱 Responsive Design**: Mobile-friendly Bootstrap interface
- **💾 History Tracking**: Complete prediction history with search and filter
- **📈 Analytics**: Detailed insights and recommendations
- **📥 PDF Reports**: Download prediction reports
- **🎨 Beautiful UI**: Modern gradient design with smooth animations

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Machine Learning**: scikit-learn (Random Forest)
- **Frontend**: Bootstrap 5, Chart.js
- **Styling**: Custom CSS with animations

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Smart-Crop-Recommendation-System.git
cd Smart-Crop-Recommendation-System
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Place required files**
- `crop_model.pkl` - Trained ML model
- `Crop_recommendation.csv` - Dataset with crop recommendations

## 📁 Project Structure

```
crop_web_app/
├── app.py
├── crop_model.pkl
├── Crop_recommendation.csv
├── history.db
├── requirements.txt
├── templates/
│   ├── dashboard.html
│   ├── input.html
│   ├── result.html
│   └── history.html
└── static/
    ├── style.css
    ├── charts.js
    └── script.js
```

## 🏃 Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📖 Usage Guide

### Dashboard
- Overview of the system
- Quick statistics
- Navigation to other pages

### Crop Prediction
1. Enter soil nutrients (N, P, K)
2. Input environmental conditions
3. Submit form
4. View detailed recommendations

### Results
- Recommended crop with confidence score
- Detailed crop information
- Visualization charts
- Download PDF report

### History
- View all previous predictions
- Search by crop name
- Delete individual records
- Clear all history

## 🎯 Supported Crops

Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Sugarcane, Tobacco, Jute

## 🔐 Input Validation

All inputs are validated for:
- Numeric values only
- Non-negative numbers
- Appropriate ranges per field
- Required fields completion

## 📊 Data Visualization

- **Crop Distribution Chart**: Bar chart showing prediction frequency
- **Feature Importance**: Pie chart showing feature weights
- **Confidence Levels**: Progress bars for model confidence

## 🌟 Key Capabilities

- **Accurate Predictions**: 94% model accuracy
- **Real-time Analysis**: Instant recommendations
- **Comprehensive Details**: Temperature, water, fertilizer requirements
- **Mobile Responsive**: Works on all devices
- **User-friendly**: Intuitive interface with tooltips

## 🔄 Workflow

1. User visits dashboard
2. Navigates to prediction page
3. Fills in soil and weather data
4. Submits form for prediction
5. Views detailed crop recommendation
6. Downloads report if needed
7. Prediction saved to history
8. Can view/search/delete from history anytime

## 💡 Tips for Better Predictions

- Ensure accurate soil nutrient measurements
- Use seasonal average temperatures
- Provide annual rainfall data
- Soil pH should be measured accurately
- All fields must have valid numeric values

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for sustainable agriculture

## 📞 Support

For issues or questions, please create an issue in the repository.

## 🎓 Educational Purpose

This project is designed for educational purposes to demonstrate:
- Flask web development
- Machine Learning integration
- Data visualization
- Database management
- Responsive web design
- REST API development

## 🚀 Future Enhancements

- Weather API integration
- Soil testing recommendations
- Fertilizer pricing recommendations
- Crop yield predictions
- Multi-language support
- Mobile app version
- Real-time weather data

---

**Happy Farming! 🌾**