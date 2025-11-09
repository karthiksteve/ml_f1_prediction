"""
Data loading utilities for F1 prediction project.
Handles FastF1 data loading with proper error handling and fallbacks.
"""
import pandas as pd
import numpy as np
import fastf1
import os
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_fastf1_cache(cache_dir: Optional[str] = None) -> None:
    """
    Setup FastF1 cache directory.
    
    Args:
        cache_dir: Directory path for cache. If None, uses default.
    """
    if cache_dir is None:
        cache_dir = os.path.join(os.getcwd(), "f1_cache")
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        logger.info(f"Created FastF1 cache directory: {cache_dir}")
    
    fastf1.Cache.enable_cache(cache_dir)
    logger.info(f"FastF1 cache enabled at: {cache_dir}")


def load_f1_session_data(
    year: int,
    round_number: int,
    session_type: str = "R",
    cache_dir: Optional[str] = None
) -> Tuple[pd.DataFrame, bool]:
    """
    Load F1 session data using FastF1.
    
    Args:
        year: Race year (e.g., 2024)
        round_number: Round number (e.g., 20 for Mexican GP)
        session_type: Session type ("R" for race, "Q" for qualifying, etc.)
        cache_dir: Cache directory path
        
    Returns:
        Tuple of (laps_dataframe, success_flag)
        If FastF1 fails, returns dummy data with success_flag=False
    """
    if cache_dir:
        setup_fastf1_cache(cache_dir)
    
    try:
        logger.info(f"Loading {year} Round {round_number} {session_type} session data via FastF1...")
        session = fastf1.get_session(year, round_number, session_type)
        session.load()
        
        # Extract relevant columns
        laps = session.laps[
            ["Driver", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]
        ].copy()
        
        # Remove rows with missing critical data
        laps.dropna(
            subset=["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"],
            inplace=True
        )
        
        if len(laps) == 0:
            raise ValueError("No valid lap data found in session")
        
        logger.info(f"Successfully loaded {len(laps)} laps from FastF1")
        return laps, True
        
    except Exception as e:
        logger.warning(f"Error loading FastF1 data: {e}. Using dummy data for demonstration.")
        return _create_dummy_lap_data(), False


def _create_dummy_lap_data() -> pd.DataFrame:
    """
    Create dummy lap data for testing when FastF1 is unavailable.
    
    Returns:
        DataFrame with dummy lap data
    """
    drivers = [
        "VER", "NOR", "PIA", "RUS", "SAI", "ALB", "LEC", "OCO",
        "HAM", "STR", "GAS", "ALO", "HUL"
    ]
    
    # Create multiple laps per driver for more realistic data
    num_laps_per_driver = 3
    all_drivers = drivers * num_laps_per_driver
    
    np.random.seed(42)  # For reproducibility
    
    laps = pd.DataFrame({
        "Driver": all_drivers,
        "LapTime": pd.to_timedelta(np.random.rand(len(all_drivers)) * 3 + 73, unit='s'),
        "Sector1Time": pd.to_timedelta(np.random.rand(len(all_drivers)) * 5 + 20, unit='s'),
        "Sector2Time": pd.to_timedelta(np.random.rand(len(all_drivers)) * 5 + 20, unit='s'),
        "Sector3Time": pd.to_timedelta(np.random.rand(len(all_drivers)) * 5 + 20, unit='s'),
    })
    
    laps.dropna(inplace=True)
    return laps


def process_sector_times(laps_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process lap data to extract sector times in seconds.
    
    Args:
        laps_df: DataFrame with lap data from FastF1
        
    Returns:
        DataFrame with aggregated sector times by driver
    """
    # Convert timedelta columns to seconds
    time_columns = ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]
    for col in time_columns:
        if col in laps_df.columns:
            laps_df[f"{col} (s)"] = laps_df[col].dt.total_seconds()
    
    # Aggregate sector times by driver
    sector_times = laps_df.groupby("Driver").agg({
        "Sector1Time (s)": "mean",
        "Sector2Time (s)": "mean",
        "Sector3Time (s)": "mean"
    }).reset_index()
    
    # Calculate total sector time
    sector_times["TotalSectorTime (s)"] = (
        sector_times["Sector1Time (s)"] +
        sector_times["Sector2Time (s)"] +
        sector_times["Sector3Time (s)"]
    )
    
    return sector_times


def get_average_lap_time(laps_df: pd.DataFrame) -> pd.Series:
    """
    Get average lap time per driver.
    
    Args:
        laps_df: DataFrame with lap data
        
    Returns:
        Series with driver codes as index and average lap times in seconds
    """
    if "LapTime (s)" not in laps_df.columns:
        laps_df["LapTime (s)"] = laps_df["LapTime"].dt.total_seconds()
    
    return laps_df.groupby("Driver")["LapTime (s)"].mean()


