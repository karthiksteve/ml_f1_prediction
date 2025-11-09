# F1 Race Prediction - Machine Learning Project

A machine learning project for predicting Formula 1 race results using historical data, weather conditions, and driver/team performance metrics.

## Features

- **Multiple ML Models**: Gradient Boosting, LightGBM, and Random Forest
- **Real F1 Data**: Uses FastF1 library to fetch real Formula 1 session data
- **Weather Integration**: Fetches weather forecasts from OpenWeatherMap API
- **Comprehensive Metrics**: MAE, MSE, RMSE, and R² score evaluation
- **Modular Design**: Clean, reusable code structure

## Project Structure

```
ml_f1_prediction/
├── ML_FINAL.ipynb          # Main Jupyter notebook with model implementations
├── config.py                # Configuration file (API keys, track data, etc.)
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── data_loader.py       # F1 data loading utilities
│   ├── weather.py           # Weather API integration
│   └── models.py            # Model training and evaluation
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root (or set environment variables):

```bash
# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_api_key_here"

# Linux/Mac
export OPENWEATHER_API_KEY="your_api_key_here"
```

Or create a `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
```

**Note**: Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

### 3. Run the Notebook

Open `ML_FINAL.ipynb` in Jupyter Notebook or JupyterLab and run the cells.

## Usage

### Using the Utility Modules

The project now includes reusable utility modules that can be imported:

```python
from utils import (
    load_f1_session_data,
    fetch_weather_data,
    train_and_evaluate
)
from config import DRIVER_FULL_NAMES, TRACK_COORDINATES

# Load F1 data
laps_data, success = load_f1_session_data(year=2024, round_number=20, session_type="R")

# Fetch weather data
temperature, rain_prob = fetch_weather_data("mexico")

# Train and evaluate a model
model, metrics, imputer = train_and_evaluate(X, y, model_type="gradient_boosting")
```

### Configuration

All configuration is centralized in `config.py`:

- **API Keys**: Set via environment variables
- **Track Coordinates**: Pre-configured for Mexico and Monaco
- **Driver/Team Mappings**: Full names and team associations
- **Model Hyperparameters**: Tuned default values

## Models

### 1. Gradient Boosting Regressor
- Default: 100 estimators, learning rate 0.1, max depth 3
- Good balance of performance and interpretability

### 2. LightGBM Regressor
- Fast training with good performance
- Handles missing values well

### 3. Random Forest Regressor
- Robust ensemble method
- Provides feature importance

## Features Used

- **Qualifying Time**: Driver's qualifying lap time
- **Rain Probability**: Weather forecast rain probability
- **Temperature**: Race day temperature
- **Team Performance Score**: Normalized championship points
- **Clean Air Race Pace**: Representative race pace
- **Average Position Change**: Historical position changes at track
- **Sector Times**: Aggregated sector time data

## Model Evaluation

Each model is evaluated using:
- **MAE** (Mean Absolute Error): Average prediction error in seconds
- **MSE** (Mean Squared Error): Penalizes larger errors more
- **RMSE** (Root Mean Squared Error): Error in same units as target
- **R² Score**: Coefficient of determination (1.0 = perfect, 0.0 = baseline)

## Improvements Made

✅ **Security**: API keys now use environment variables  
✅ **Code Organization**: Modular utilities reduce duplication  
✅ **Error Handling**: Robust error handling with fallbacks  
✅ **Configuration**: Centralized configuration management  
✅ **Documentation**: Comprehensive docstrings and README  
✅ **Type Hints**: Added type annotations for better code clarity  
✅ **Best Practices**: Following Python best practices

## Troubleshooting

### FastF1 Data Loading Fails
- The code automatically falls back to dummy data
- Check your internet connection
- FastF1 may cache data in `f1_cache/` directory

### Weather API Errors
- Verify your API key is set correctly
- Check API key has forecast access enabled
- Default values will be used if API fails

### LightGBM Import Error
```bash
pip install lightgbm
```

## Contributing

Feel free to submit issues or pull requests!

## License

This project is for educational purposes.

## Acknowledgments

- [FastF1](https://github.com/theOehrly/Fast-F1) for F1 data
- [OpenWeatherMap](https://openweathermap.org/) for weather data
- Scikit-learn, LightGBM, and other ML libraries


