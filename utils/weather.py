"""
Weather data fetching utilities for F1 prediction project.
Handles OpenWeatherMap API calls with proper error handling.
"""
import requests
from typing import Tuple, Optional
import logging
from config import (
    get_weather_api_key,
    get_track_coordinates,
    DEFAULT_TEMPERATURE,
    DEFAULT_RAIN_PROBABILITY,
    RACE_FORECAST_TIMES,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_weather_data(
    track_name: str,
    forecast_time: Optional[str] = None,
    timeout: int = 5
) -> Tuple[float, float]:
    """
    Fetch weather data for a specific track and time.
    
    Args:
        track_name: Name of the track (e.g., "mexico", "monaco")
        forecast_time: Forecast time in format "YYYY-MM-DD HH:MM:SS" (UTC).
                      If None, uses default from config.
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (temperature_celsius, rain_probability)
        Returns defaults if API call fails
    """
    # Get coordinates and API key
    try:
        lat, lon = get_track_coordinates(track_name)
        api_key = get_weather_api_key()
    except ValueError as e:
        logger.warning(f"Configuration error: {e}. Using default weather values.")
        return DEFAULT_TEMPERATURE, DEFAULT_RAIN_PROBABILITY
    
    # Use default forecast time if not provided
    if forecast_time is None:
        forecast_time = RACE_FORECAST_TIMES.get(track_name.lower())
        if forecast_time is None:
            logger.warning(
                f"No forecast time configured for {track_name}. "
                f"Using default values."
            )
            return DEFAULT_TEMPERATURE, DEFAULT_RAIN_PROBABILITY
    
    # Build API URL
    weather_url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    
    logger.info(f"Fetching weather data for {track_name}...")
    
    try:
        response = requests.get(weather_url, timeout=timeout)
        response.raise_for_status()
        weather_data = response.json()
        
        # Validate response structure
        if "list" not in weather_data:
            if "message" in weather_data:
                raise ValueError(
                    f"API Error: {weather_data.get('message', 'Unknown error')}"
                )
            raise KeyError("API response does not contain 'list' key")
        
        # Find matching forecast
        forecast_data = next(
            (f for f in weather_data["list"] if f.get("dt_txt") == forecast_time),
            None
        )
        
        if forecast_data:
            rain_probability = forecast_data.get("pop", 0)
            temperature = forecast_data.get("main", {}).get("temp", DEFAULT_TEMPERATURE)
            logger.info(
                f"✅ Weather forecast loaded: Temp={temperature}°C, "
                f"Rain Prob={rain_probability*100:.0f}%"
            )
            return temperature, rain_probability
        else:
            logger.info(
                f"ℹ️ Weather data found but no exact forecast for {forecast_time}. "
                f"Using defaults (T={DEFAULT_TEMPERATURE}°C, R={DEFAULT_RAIN_PROBABILITY})."
            )
            return DEFAULT_TEMPERATURE, DEFAULT_RAIN_PROBABILITY
            
    except requests.exceptions.RequestException as e:
        logger.warning(
            f"❌ Weather API connection failure: {e}. "
            f"Using default values (T={DEFAULT_TEMPERATURE}°C, R={DEFAULT_RAIN_PROBABILITY})."
        )
        return DEFAULT_TEMPERATURE, DEFAULT_RAIN_PROBABILITY
    except (KeyError, ValueError) as e:
        logger.warning(
            f"❌ Weather API failure: {e}. "
            f"Using default values (T={DEFAULT_TEMPERATURE}°C, R={DEFAULT_RAIN_PROBABILITY})."
        )
        return DEFAULT_TEMPERATURE, DEFAULT_RAIN_PROBABILITY


