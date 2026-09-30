# =========================================================
# TRUCK INPUT FIELD CONFIGURATION
# =========================================================

NUMERIC_FIELDS = [
    "Driver_Age",
    "Driving_Hours",
    "Speed",
    "Harsh_Braking",
    "Harsh_Acceleration",
    "Drowsiness_Score",
    "Engine_Temperature",
    "Engine_Vibration",
    "Battery_Voltage",
    "Oil_Pressure",
    "Tyre_Pressure",
    "Vehicle_Age",
    "Mileage",
    "Previous_Breakdowns",
    "Previous_Accidents"
]


CATEGORICAL_FIELDS = {
    "Weather": [
        "Clear",
        "Rain",
        "Fog",
        "Snow"
    ],
    "Road_Type": [
        "Highway",
        "City",
        "Rural"
    ]
}

def get_risk_message(risk_label):
    """
    Return a user-friendly message
    based on the predicted risk level.
    """

    if risk_label == "High Risk":
        return "⚠️ High Risk Detected - Immediate attention is recommended."

    return "✅ Low Risk - The truck appears to be operating safely."


def format_probability(probability):
    """
    Convert probability into percentage format.
    """

    return f"{probability * 100:.2f}%"

def validate_input(data):
    """
    Check whether all required input fields are present.
    """

    required_fields = NUMERIC_FIELDS + list(
        CATEGORICAL_FIELDS.keys()
    )

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return False, missing_fields

    return True, []


