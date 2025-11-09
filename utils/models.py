"""
Model training and evaluation utilities for F1 prediction project.
Provides reusable functions for training different ML models.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from typing import Dict, Tuple, Any, Optional
import logging

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    logging.warning("LightGBM not available. Install with: pip install lightgbm")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_features(
    data: pd.DataFrame,
    feature_columns: list,
    imputer: Optional[SimpleImputer] = None
) -> Tuple[pd.DataFrame, SimpleImputer]:
    """
    Prepare features for model training.
    
    Args:
        data: DataFrame with feature columns
        feature_columns: List of column names to use as features
        imputer: Pre-fitted imputer. If None, creates and fits a new one.
        
    Returns:
        Tuple of (imputed_features_df, fitted_imputer)
    """
    X = data[feature_columns].copy()
    
    if imputer is None:
        imputer = SimpleImputer(strategy="median")
        X_imputed = imputer.fit_transform(X)
    else:
        X_imputed = imputer.transform(X)
    
    X_imputed = pd.DataFrame(
        X_imputed,
        columns=X.columns,
        index=X.index
    )
    
    return X_imputed, imputer


def train_gradient_boosting(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: Optional[Dict[str, Any]] = None
) -> GradientBoostingRegressor:
    """
    Train a Gradient Boosting Regressor model.
    
    Args:
        X_train: Training features
        y_train: Training targets
        config: Model configuration dict. Uses defaults if None.
        
    Returns:
        Trained GradientBoostingRegressor
    """
    from config import MODEL_CONFIG
    
    if config is None:
        config = MODEL_CONFIG["gradient_boosting"]
    
    logger.info("Training Gradient Boosting Regressor...")
    model = GradientBoostingRegressor(**config)
    model.fit(X_train, y_train)
    
    return model


def train_lightgbm(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Train a LightGBM Regressor model.
    
    Args:
        X_train: Training features
        y_train: Training targets
        config: Model configuration dict. Uses defaults if None.
        
    Returns:
        Trained LightGBM model
        
    Raises:
        ImportError: If LightGBM is not installed
    """
    if not LIGHTGBM_AVAILABLE:
        raise ImportError("LightGBM is not installed. Install with: pip install lightgbm")
    
    from config import MODEL_CONFIG
    
    if config is None:
        config = MODEL_CONFIG["lightgbm"]
    
    logger.info("Training LightGBM Regressor...")
    
    # Clean feature names (LightGBM doesn't like spaces)
    X_train_clean = X_train.copy()
    X_train_clean.columns = [col.replace(" ", "_") for col in X_train_clean.columns]
    
    model = lgb.LGBMRegressor(**config)
    model.fit(X_train_clean, y_train)
    
    return model


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: Optional[Dict[str, Any]] = None
) -> RandomForestRegressor:
    """
    Train a Random Forest Regressor model.
    
    Args:
        X_train: Training features
        y_train: Training targets
        config: Model configuration dict. Uses defaults if None.
        
    Returns:
        Trained RandomForestRegressor
    """
    from config import MODEL_CONFIG
    
    if config is None:
        config = MODEL_CONFIG["random_forest"]
    
    logger.info("Training Random Forest Regressor...")
    model = RandomForestRegressor(**config)
    model.fit(X_train, y_train)
    
    return model


def evaluate_model(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str = "Model"
) -> Dict[str, float]:
    """
    Evaluate a trained model and return metrics.
    
    Args:
        model: Trained model (must have .predict method)
        X_test: Test features
        y_test: Test targets
        model_name: Name of the model for logging
        
    Returns:
        Dictionary with evaluation metrics
    """
    # Handle LightGBM feature name cleaning
    if hasattr(model, '__class__') and 'LGBM' in str(model.__class__):
        X_test_clean = X_test.copy()
        X_test_clean.columns = [col.replace(" ", "_") for col in X_test_clean.columns]
        y_pred = model.predict(X_test_clean)
    else:
        y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
    }
    
    logger.info(f"\n{model_name} Evaluation:")
    logger.info(f"  Mean Absolute Error (MAE): {mae:.3f} seconds")
    logger.info(f"  Mean Squared Error (MSE): {mse:.3f} seconds²")
    logger.info(f"  Root Mean Squared Error (RMSE): {rmse:.3f} seconds")
    logger.info(f"  R-squared (R²) Score: {r2:.3f}")
    
    return metrics


def train_and_evaluate(
    X: pd.DataFrame,
    y: pd.Series,
    model_type: str = "gradient_boosting",
    test_size: float = 0.3,
    random_state: int = 37,
    model_config: Optional[Dict[str, Any]] = None
) -> Tuple[Any, Dict[str, float], SimpleImputer]:
    """
    Complete pipeline: prepare data, train model, and evaluate.
    
    Args:
        X: Feature DataFrame
        y: Target Series
        model_type: Type of model ("gradient_boosting", "lightgbm", "random_forest")
        test_size: Proportion of data for testing
        random_state: Random seed
        model_config: Optional model configuration
        
    Returns:
        Tuple of (trained_model, evaluation_metrics, fitted_imputer)
    """
    from config import MODEL_CONFIG
    
    # Prepare features
    X_imputed, imputer = prepare_features(X, X.columns.tolist())
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed, y, test_size=test_size, random_state=random_state
    )
    
    # Train model
    if model_type == "gradient_boosting":
        model = train_gradient_boosting(X_train, y_train, model_config)
    elif model_type == "lightgbm":
        model = train_lightgbm(X_train, y_train, model_config)
    elif model_type == "random_forest":
        model = train_random_forest(X_train, y_train, model_config)
    else:
        raise ValueError(
            f"Unknown model_type: {model_type}. "
            f"Choose from: gradient_boosting, lightgbm, random_forest"
        )
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test, model_type)
    
    return model, metrics, imputer


