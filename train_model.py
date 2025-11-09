"""
Main training script for F1 race prediction models.
This script demonstrates how to use the utility modules to train models.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any

from config import (
    DRIVER_FULL_NAMES,
    DRIVER_TO_TEAM,
    TEAM_PERFORMANCE_SCORE,
    CLEAN_AIR_RACE_PACE,
    AVERAGE_POSITION_CHANGE,
    MODEL_CONFIG,
)
from utils import (
    load_f1_session_data,
    process_sector_times,
    get_average_lap_time,
    fetch_weather_data,
    train_and_evaluate,
    prepare_features,
)
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_qualifying_data(track_name: str) -> pd.DataFrame:
    """
    Create qualifying data for a specific track.
    In a real scenario, this would fetch from FastF1 or another data source.
    
    Args:
        track_name: Name of the track (e.g., "mexico", "monaco")
        
    Returns:
        DataFrame with qualifying data
    """
    # Example qualifying times - replace with real data
    qualifying_data = {
        "mexico": {
            "Driver": ["VER", "NOR", "PIA", "RUS", "SAI", "ALB", "LEC", "OCO",
                      "HAM", "STR", "GAS", "ALO", "HUL"],
            "QualifyingTime (s)": [
                71.350, 71.800, 71.950, 72.050, 72.150, 72.400, 71.700, 72.500,
                71.900, 72.800, 72.700, 72.300, 72.600
            ]
        },
        "monaco": {
            "Driver": ["VER", "NOR", "PIA", "RUS", "SAI", "ALB", "LEC", "OCO",
                      "HAM", "STR", "GAS", "ALO", "HUL"],
            "QualifyingTime (s)": [
                70.669, 69.954, 70.129, np.nan, 71.362, 71.213, 70.063, 70.942,
                70.382, 72.563, 71.994, 70.924, 71.596
            ]
        }
    }
    
    if track_name.lower() not in qualifying_data:
        raise ValueError(f"Track '{track_name}' not found in qualifying data")
    
    data = qualifying_data[track_name.lower()]
    qualifying_df = pd.DataFrame(data)
    
    # Add derived features
    qualifying_df["CleanAirRacePace (s)"] = qualifying_df["Driver"].map(
        CLEAN_AIR_RACE_PACE.get(track_name.lower(), {})
    )
    qualifying_df["Team"] = qualifying_df["Driver"].map(DRIVER_TO_TEAM)
    qualifying_df["TeamPerformanceScore"] = qualifying_df["Team"].map(TEAM_PERFORMANCE_SCORE)
    qualifying_df["AveragePositionChange"] = qualifying_df["Driver"].map(
        AVERAGE_POSITION_CHANGE.get(track_name.lower(), {})
    )
    
    return qualifying_df


def prepare_training_data(
    track_name: str,
    year: int = 2024,
    round_number: int = 20
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare complete training dataset.
    
    Args:
        track_name: Name of the track
        year: Year of historical race data
        round_number: Round number for the race
        
    Returns:
        Tuple of (features_df, target_series)
    """
    # Load F1 session data
    laps_data, success = load_f1_session_data(year, round_number, session_type="R")
    
    # Process sector times
    sector_times = process_sector_times(laps_data)
    
    # Get average lap times (target variable)
    avg_lap_times = get_average_lap_time(laps_data)
    
    # Create qualifying data
    qualifying_df = create_qualifying_data(track_name)
    
    # Fetch weather data
    temperature, rain_prob = fetch_weather_data(track_name)
    
    # Merge all data
    merged_data = qualifying_df.merge(
        sector_times[["Driver", "TotalSectorTime (s)"]],
        on="Driver",
        how="left"
    )
    
    # Add weather features
    merged_data["RainProbability"] = rain_prob
    merged_data["Temperature"] = temperature
    
    # Filter to drivers present in both datasets
    valid_drivers = merged_data["Driver"].isin(laps_data["Driver"].unique())
    merged_data = merged_data[valid_drivers].copy()
    
    # Add full names for output
    merged_data["Driver (Full Name)"] = merged_data["Driver"].map(DRIVER_FULL_NAMES)
    merged_data["Team (Full Name)"] = merged_data["Team"]
    
    # Define features
    feature_columns = [
        "QualifyingTime (s)",
        "RainProbability",
        "Temperature",
        "TeamPerformanceScore",
        "CleanAirRacePace (s)",
        "AveragePositionChange"
    ]
    
    # Prepare target (y)
    y = avg_lap_times.reindex(merged_data["Driver"]).fillna(avg_lap_times.mean())
    
    # Prepare features (X)
    X = merged_data[feature_columns].copy()
    X.columns = [col.replace(" (s)", "") for col in X.columns]  # Clean column names
    
    return X, y, merged_data


def main():
    """Main training function."""
    logger.info("=" * 60)
    logger.info("F1 Race Prediction - Model Training")
    logger.info("=" * 60)
    
    # Configuration
    track_name = "mexico"  # Change to "monaco" for Monaco GP
    year = 2024
    round_number = 20  # Mexican GP
    
    # Prepare data
    logger.info(f"\nPreparing data for {track_name.upper()} GP...")
    X, y, merged_data = prepare_training_data(track_name, year, round_number)
    
    logger.info(f"Training data shape: {X.shape}")
    logger.info(f"Number of drivers: {len(y)}")
    
    # Train models
    models_to_train = ["gradient_boosting", "random_forest"]
    
    # Check for LightGBM availability
    try:
        import lightgbm as lgb
        models_to_train.append("lightgbm")
    except ImportError:
        logger.warning("LightGBM not available. Skipping LightGBM model.")
    
    results = {}
    
    for model_type in models_to_train:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Training {model_type.upper()} model...")
        logger.info(f"{'=' * 60}")
        
        try:
            model, metrics, imputer = train_and_evaluate(
                X, y,
                model_type=model_type,
                test_size=MODEL_CONFIG["test_size"],
                random_state=MODEL_CONFIG["random_state"]
            )
            
            # Make predictions
            X_imputed, _ = prepare_features(X, X.columns.tolist(), imputer)
            predictions = model.predict(X_imputed)
            
            # Store results
            results[model_type] = {
                "model": model,
                "metrics": metrics,
                "predictions": predictions,
            }
            
            # Create results dataframe
            results_df = merged_data.copy()
            results_df["PredictedRaceTime (s)"] = predictions
            results_df = results_df.sort_values("PredictedRaceTime (s)")
            
            # Display top 3
            logger.info("\n🏆 Predicted Top 3 🏆")
            for i, (idx, row) in enumerate(results_df.head(3).iterrows(), 1):
                medal = ["🥇", "🥈", "🥉"][i - 1]
                logger.info(
                    f"{medal} P{i}: {row['Driver (Full Name)']} "
                    f"({row['Team (Full Name)']}) "
                    f"({row['PredictedRaceTime (s)']:.3f} s)"
                )
            
        except Exception as e:
            logger.error(f"Error training {model_type}: {e}")
            continue
    
    # Compare models
    if len(results) > 1:
        logger.info("\n" + "=" * 60)
        logger.info("Model Comparison")
        logger.info("=" * 60)
        for model_name, result in results.items():
            metrics = result["metrics"]
            logger.info(
                f"{model_name.upper()}: "
                f"MAE={metrics['MAE']:.3f}s, "
                f"RMSE={metrics['RMSE']:.3f}s, "
                f"R²={metrics['R2']:.3f}"
            )
    
    logger.info("\n✅ Training complete!")


if __name__ == "__main__":
    main()

