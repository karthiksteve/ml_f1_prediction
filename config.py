"""
Configuration file for F1 Prediction Project
Handles API keys, track coordinates, and other configuration settings.
"""
import os
from typing import Dict, Tuple, Optional

# API Configuration
# Get API key from environment variable for security
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Track Coordinates (lat, lon)
TRACK_COORDINATES: Dict[str, Tuple[float, float]] = {
    "mexico": (19.40, -99.10),  # Autódromo Hermanos Rodríguez, Mexico City
    "monaco": (43.7384, 7.4246),  # Circuit de Monaco
}

# Driver Full Names Mapping
DRIVER_FULL_NAMES: Dict[str, str] = {
    "VER": "Max Verstappen",
    "NOR": "Lando Norris",
    "PIA": "Oscar Piastri",
    "RUS": "George Russell",
    "SAI": "Carlos Sainz",
    "ALB": "Alexander Albon",
    "LEC": "Charles Leclerc",
    "OCO": "Esteban Ocon",
    "HAM": "Lewis Hamilton",
    "STR": "Lance Stroll",
    "GAS": "Pierre Gasly",
    "ALO": "Fernando Alonso",
    "HUL": "Nico Hülkenberg",
    "TSU": "Yuki Tsunoda",
}

# Team Mapping
DRIVER_TO_TEAM: Dict[str, str] = {
    "VER": "Red Bull Racing",
    "NOR": "McLaren",
    "PIA": "McLaren",
    "LEC": "Ferrari",
    "RUS": "Mercedes",
    "HAM": "Mercedes",
    "GAS": "Alpine",
    "ALO": "Aston Martin",
    "TSU": "Racing Bulls",
    "SAI": "Ferrari",
    "HUL": "Kick Sauber",
    "OCO": "Alpine",
    "STR": "Aston Martin",
    "ALB": "Williams",
}

# Team Performance Scores (based on championship points)
TEAM_POINTS: Dict[str, int] = {
    "McLaren": 279,
    "Mercedes": 147,
    "Red Bull Racing": 131,
    "Williams": 51,
    "Ferrari": 114,
    "Haas": 20,
    "Aston Martin": 14,
    "Kick Sauber": 6,
    "Racing Bulls": 10,
    "Alpine": 7,
}

# Normalize team performance scores
MAX_POINTS = max(TEAM_POINTS.values())
TEAM_PERFORMANCE_SCORE: Dict[str, float] = {
    team: points / MAX_POINTS for team, points in TEAM_POINTS.items()
}

# Model Configuration
MODEL_CONFIG = {
    "test_size": 0.3,
    "random_state": 37,
    "gradient_boosting": {
        "n_estimators": 100,
        "learning_rate": 0.1,  # Reduced from 0.7 for better generalization
        "max_depth": 3,
        "random_state": 37,
    },
    "lightgbm": {
        "n_estimators": 100,
        "learning_rate": 0.1,  # Reduced from 0.7 for better generalization
        "max_depth": 3,
        "random_state": 37,
    },
    "random_forest": {
        "n_estimators": 100,
        "random_state": 37,
        "max_depth": 10,
        "min_samples_split": 2,
    },
}

# FastF1 Cache Configuration
F1_CACHE_DIR = os.path.join(os.getcwd(), "f1_cache")

# Default Weather Values
DEFAULT_TEMPERATURE = 22  # Celsius
DEFAULT_RAIN_PROBABILITY = 0.0

# Race Forecast Times (format: "YYYY-MM-DD HH:MM:SS")
RACE_FORECAST_TIMES: Dict[str, str] = {
    "mexico": "2025-10-26 20:00:00",  # UTC
    "monaco": "2025-05-25 13:00:00",  # UTC
}

# Clean Air Race Pace (representative lap times in seconds)
CLEAN_AIR_RACE_PACE: Dict[str, Dict[str, float]] = {
    "mexico": {
        "VER": 74.800,
        "HAM": 75.350,
        "LEC": 74.950,
        "NOR": 74.900,
        "ALO": 75.600,
        "PIA": 75.050,
        "RUS": 75.300,
        "SAI": 75.200,
        "STR": 75.800,
        "HUL": 76.100,
        "OCO": 76.250,
        "ALB": 75.900,
        "GAS": 76.300,
    },
    "monaco": {
        "VER": 93.191067,
        "HAM": 94.020622,
        "LEC": 93.418667,
        "NOR": 93.428600,
        "ALO": 94.784333,
        "PIA": 93.232111,
        "RUS": 93.833378,
        "SAI": 94.497444,
        "STR": 95.318250,
        "HUL": 95.345455,
        "OCO": 95.682128,
    },
}

# Average Position Change (qualifying position - finish position)
# Positive means losing positions, negative means gaining positions
AVERAGE_POSITION_CHANGE: Dict[str, Dict[str, float]] = {
    "mexico": {
        "VER": -0.5,
        "NOR": 1.5,
        "PIA": 1.0,
        "RUS": -0.2,
        "SAI": 0.8,
        "ALB": 1.5,
        "LEC": 0.5,
        "OCO": 1.2,
        "HAM": -0.4,
        "STR": 2.0,
        "GAS": 0.7,
        "ALO": 0.0,
        "HUL": 1.0,
    },
    "monaco": {
        "VER": -1.0,
        "NOR": 1.0,
        "PIA": 0.2,
        "RUS": 0.5,
        "SAI": -0.3,
        "ALB": 0.8,
        "LEC": -1.5,
        "OCO": -0.2,
        "HAM": 0.3,
        "STR": 1.1,
        "GAS": -0.4,
        "ALO": -0.6,
        "HUL": 0.0,
    },
}


def get_weather_api_key() -> str:
    """Get OpenWeatherMap API key from environment or raise error."""
    api_key = OPENWEATHER_API_KEY
    if not api_key:
        raise ValueError(
            "OPENWEATHER_API_KEY environment variable is not set. "
            "Please set it using: export OPENWEATHER_API_KEY='your_key_here'"
        )
    return api_key


def get_track_coordinates(track_name: str) -> Tuple[float, float]:
    """Get track coordinates by track name."""
    track_name_lower = track_name.lower()
    if track_name_lower not in TRACK_COORDINATES:
        raise ValueError(
            f"Track '{track_name}' not found. Available tracks: {list(TRACK_COORDINATES.keys())}"
        )
    return TRACK_COORDINATES[track_name_lower]


