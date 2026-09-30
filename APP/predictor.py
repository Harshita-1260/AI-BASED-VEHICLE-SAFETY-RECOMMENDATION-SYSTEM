import joblib
import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"


# Existing model file paths
DRIVER_MODEL_PATH = MODELS_DIR / "driver_safety_model.pkl"
BREAKDOWN_MODEL_PATH = MODELS_DIR / "breakdown_model.pkl"

# Existing preprocessor files
DRIVER_PREPROCESSOR_PATH = MODELS_DIR / "driver_preprocessor.pkl"
VEHICLE_PREPROCESSOR_PATH = MODELS_DIR / "vehicle_preprocessor.pkl"

# Final configuration file
CONFIG_PATH = MODELS_DIR / "model_config.pkl"


# =========================================================
# LOAD MODELS
# =========================================================

driver_safety_model = joblib.load(DRIVER_MODEL_PATH)
breakdown_model = joblib.load(BREAKDOWN_MODEL_PATH)


# Load existing preprocessors
# These files are preserved, but are not separately applied because
# the saved models already handle preprocessing internally.
driver_preprocessor = joblib.load(DRIVER_PREPROCESSOR_PATH)
vehicle_preprocessor = joblib.load(VEHICLE_PREPROCESSOR_PATH)


# Load final model configuration
model_config = joblib.load(CONFIG_PATH)

# Final Breakdown Risk threshold
BREAKDOWN_THRESHOLD = model_config["breakdown_threshold"]


print("All models and configurations loaded successfully")
print("Breakdown Threshold:", BREAKDOWN_THRESHOLD)


# =========================================================
# INPUT PREPARATION
# =========================================================

def prepare_input(data):
    """
    Convert user input dictionary into
    a pandas DataFrame for prediction.
    """

    input_df = pd.DataFrame([data])

    return input_df


# =========================================================
# DRIVER SAFETY PREDICTION
# =========================================================

def predict_driver_risk(data):
    """
    Predict Driver Safety Risk.
    """

    # Convert dictionary to DataFrame
    input_df = prepare_input(data)

    # Saved model handles preprocessing internally
    prediction = driver_safety_model.predict(input_df)[0]

    # Get High-Risk probability
    probability = driver_safety_model.predict_proba(
        input_df
    )[0, 1]

    # Convert prediction to readable label
    risk_label = (
        "High Risk"
        if prediction == 1
        else "Low Risk"
    )

    return {
        "prediction": int(prediction),
        "risk_label": risk_label,
        "high_risk_probability": round(
            float(probability), 4
        )
    }


# =========================================================
# BREAKDOWN RISK PREDICTION
# =========================================================

def predict_breakdown_risk(data):
    """
    Predict Vehicle Breakdown Risk.

    Uses the final threshold stored in
    model_config.pkl.
    """

    # Convert dictionary to DataFrame
    input_df = prepare_input(data)

    # Get High-Risk probability
    # Saved model handles preprocessing internally
    probability = breakdown_model.predict_proba(
        input_df
    )[0, 1]

    # Apply final threshold = 0.40
    prediction = int(
        probability >= BREAKDOWN_THRESHOLD
    )

    # Convert prediction to readable label
    risk_label = (
        "High Risk"
        if prediction == 1
        else "Low Risk"
    )

    return {
        "prediction": prediction,
        "risk_label": risk_label,
        "high_risk_probability": round(
            float(probability), 4
        ),
        "threshold": BREAKDOWN_THRESHOLD
    }

