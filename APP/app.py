import streamlit as st
from pathlib import Path

from predictor import (
    predict_driver_risk,
    predict_breakdown_risk
)

from utils import (
    CATEGORICAL_FIELDS,
    validate_input
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Heavy Vehicle Safety With AI",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "driver_result" not in st.session_state:
    st.session_state.driver_result = None

if "breakdown_result" not in st.session_state:
    st.session_state.breakdown_result = None

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False


# =========================================================
# PROJECT PATH
# =========================================================

APP_DIR = Path(__file__).resolve().parent

# Image is directly inside the app folder
HERO_IMAGE_PATH = APP_DIR / "heavy_vehicle.png"


# =========================================================
# PROFESSIONAL AI DASHBOARD STYLING
# =========================================================

st.markdown(
    """
    <style>

        /* Main background */
        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    #16324f 0%,
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #07131f 0%,
                    #0d1f2d 55%,
                    #07131f 100%
                );
            color: #ffffff;
        }

        /* Main content spacing */
        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Hide Streamlit branding */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        /* AI badge */
        .ai-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #5ce1e6;
            background: rgba(0, 229, 255, 0.08);
            border: 1px solid rgba(0, 229, 255, 0.35);
            margin-bottom: 1rem;
        }

        /* Main title */
        .hero-title {
            font-size: 3.2rem;
            font-weight: 800;
            letter-spacing: 1px;
            line-height: 1.1;
            margin-bottom: 0.8rem;

            background: linear-gradient(
                90deg,
                #ffffff,
                #4fc3f7,
                #00e5ff
            );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Subtitle */
        .hero-subtitle {
            font-size: 1.1rem;
            color: #a8c7d9;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }

        /* Section title */
        .section-title {
            font-size: 1.7rem;
            font-weight: 700;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #ffffff;
        }

        /* Glass card */
        .glass-card {
            background: rgba(16, 35, 50, 0.82);
            border: 1px solid rgba(120, 200, 230, 0.18);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
        }

        /* Input labels */
        .stNumberInput label,
        .stSelectbox label {
            color: #dcebf3 !important;
            font-weight: 600 !important;
        }

        /* Button */
        .stButton > button {
            width: 100%;
            border: none;
            border-radius: 12px;
            padding: 0.85rem;
            font-size: 1rem;
            font-weight: 700;
            color: #07131f;

            background: linear-gradient(
                90deg,
                #00e5ff,
                #4fc3f7
            );

            transition: 0.3s;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
        }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO SECTION
# =========================================================

hero_left, hero_right = st.columns(
    [1.2, 1],
    gap="large",
    vertical_alignment="center"
)


with hero_left:

    st.markdown(
        """
        <div class="ai-badge">
            🤖 AI-POWERED SAFETY INTELLIGENCE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-title">
            HEAVY VEHICLE<br>
            SAFETY WITH AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Intelligent risk prediction system for monitoring
            <b>Driver Safety</b> and
            <b>Vehicle Breakdown Risk</b>
            using machine learning.
        </div>
        """,
        unsafe_allow_html=True
    )


with hero_right:

    if HERO_IMAGE_PATH.exists():

        st.image(
            HERO_IMAGE_PATH,
            width="stretch"
        )

    else:

        st.warning(
            "heavy_vehicle.png not found inside the app folder."
        )


# =========================================================
# VEHICLE SAFETY INPUT DASHBOARD
# =========================================================

st.markdown(
    '<div class="section-title">🚛 Vehicle Safety Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        Enter real-time driver and vehicle parameters to analyze
        driver safety and potential breakdown risk.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INPUT FORM
# =========================================================

with st.form("vehicle_safety_form"):

    # -----------------------------------------------------
    # DRIVER BEHAVIOR
    # -----------------------------------------------------

    st.markdown("### 👤 Driver Behavior")

    col1, col2, col3 = st.columns(3)

    with col1:

        driver_age = st.number_input(
            "Driver Age",
            min_value=18,
            max_value=80,
            value=35
        )

        driving_hours = st.number_input(
            "Driving Hours",
            min_value=0.0,
            max_value=24.0,
            value=8.0,
            step=0.1
        )

    with col2:

        speed = st.number_input(
            "Vehicle Speed",
            min_value=0,
            max_value=200,
            value=60
        )

        harsh_braking = st.number_input(
            "Harsh Braking",
            min_value=0,
            value=0
        )

    with col3:

        harsh_acceleration = st.number_input(
            "Harsh Acceleration",
            min_value=0,
            value=0
        )

        drowsiness_score = st.number_input(
            "Drowsiness Score",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=0.1
        )


    st.divider()


    # -----------------------------------------------------
    # VEHICLE HEALTH
    # -----------------------------------------------------

    st.markdown("### 🔧 Vehicle Health")

    col1, col2, col3 = st.columns(3)

    with col1:

        engine_temperature = st.number_input(
            "Engine Temperature",
            value=90.0,
            step=0.1
        )

        engine_vibration = st.number_input(
            "Engine Vibration",
            min_value=0.0,
            value=2.0,
            step=0.1
        )

        battery_voltage = st.number_input(
            "Battery Voltage",
            min_value=0.0,
            value=12.5,
            step=0.1
        )

    with col2:

        oil_pressure = st.number_input(
            "Oil Pressure",
            min_value=0.0,
            value=45.0,
            step=0.1
        )

        tyre_pressure = st.number_input(
            "Tyre Pressure",
            min_value=0.0,
            value=35.0,
            step=0.1
        )

        vehicle_age = st.number_input(
            "Vehicle Age",
            min_value=0,
            value=5
        )

    with col3:

        mileage = st.number_input(
            "Mileage",
            min_value=0,
            value=200000
        )

        previous_breakdowns = st.number_input(
            "Previous Breakdowns",
            min_value=0,
            value=0
        )

        previous_accidents = st.number_input(
            "Previous Accidents",
            min_value=0,
            value=0
        )


    st.divider()


    # -----------------------------------------------------
    # ROAD CONDITIONS
    # -----------------------------------------------------

    st.markdown("### 🌦️ Road & Environment")

    col1, col2 = st.columns(2)

    with col1:

        weather = st.selectbox(
            "Weather Condition",
            CATEGORICAL_FIELDS["Weather"]
        )

    with col2:

        road_type = st.selectbox(
            "Road Type",
            CATEGORICAL_FIELDS["Road_Type"]
        )


    st.divider()


    # -----------------------------------------------------
    # PREDICTION BUTTON
    # -----------------------------------------------------

    predict_clicked = st.form_submit_button(
        "🔍 ANALYZE VEHICLE SAFETY & BREAKDOWN RISK",
        use_container_width=True
    )


# =========================================================
# AI PREDICTION LOGIC
# =========================================================

if predict_clicked:

    input_data = {
        "Driver_Age": driver_age,
        "Driving_Hours": driving_hours,
        "Speed": speed,
        "Harsh_Braking": harsh_braking,
        "Harsh_Acceleration": harsh_acceleration,
        "Drowsiness_Score": drowsiness_score,
        "Engine_Temperature": engine_temperature,
        "Engine_Vibration": engine_vibration,
        "Battery_Voltage": battery_voltage,
        "Oil_Pressure": oil_pressure,
        "Tyre_Pressure": tyre_pressure,
        "Vehicle_Age": vehicle_age,
        "Mileage": mileage,
        "Previous_Breakdowns": previous_breakdowns,
        "Previous_Accidents": previous_accidents,
        "Weather": weather,
        "Road_Type": road_type
    }


    # Validate inputs
    is_valid, missing_fields = validate_input(
        input_data
    )


    if not is_valid:

        st.error(
            f"Missing required fields: "
            f"{', '.join(missing_fields)}"
        )

        st.session_state.analysis_completed = False

    else:

        # Run Driver Safety Model
        st.session_state.driver_result = (
            predict_driver_risk(input_data)
        )

        # Run Breakdown Risk Model
        st.session_state.breakdown_result = (
            predict_breakdown_risk(input_data)
        )

        # Mark analysis as completed
        st.session_state.analysis_completed = True


# =========================================================
# PROFESSIONAL AI ANALYSIS RESULTS
# =========================================================

if (
    st.session_state.analysis_completed
    and st.session_state.driver_result is not None
    and st.session_state.breakdown_result is not None
):

    # -----------------------------------------------------
    # GET RESULTS
    # -----------------------------------------------------

    driver_result = st.session_state.driver_result

    breakdown_result = (
        st.session_state.breakdown_result
    )


    driver_risk_label = (
        driver_result["risk_label"]
    )

    driver_probability = (
        driver_result["high_risk_probability"]
    )


    breakdown_risk_label = (
        breakdown_result["risk_label"]
    )

    breakdown_probability = (
        breakdown_result["high_risk_probability"]
    )

    threshold = breakdown_result["threshold"]


    # -----------------------------------------------------
    # STATUS FUNCTION
    # -----------------------------------------------------

    def get_status_details(risk_label):

        if risk_label == "High Risk":

            return {
                "icon": "🚨",
                "status": "HIGH RISK",
                "message": (
                    "Immediate attention is recommended."
                )
            }

        return {
            "icon": "🟢",
            "status": "LOW RISK",
            "message": (
                "No immediate safety concern detected."
            )
        }


    driver_status = get_status_details(
        driver_risk_label
    )

    breakdown_status = get_status_details(
        breakdown_risk_label
    )


    # -----------------------------------------------------
    # RESULTS HEADING
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 AI Safety Analysis Results'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        "AI safety analysis completed successfully!"
    )


    # -----------------------------------------------------
    # RESULT COLUMNS
    # -----------------------------------------------------

    driver_col, breakdown_col = st.columns(
        2,
        gap="large"
    )


    # =====================================================
    # DRIVER SAFETY RESULT
    # =====================================================

    with driver_col:

        st.markdown("### 👤 Driver Safety")

        st.metric(
            label=(
                f"{driver_status['icon']} "
                "Risk Status"
            ),
            value=driver_status["status"],
            border=True
        )

        st.caption(
            "High-Risk Probability"
        )

        st.progress(
            driver_probability
        )

        st.markdown(
            f"""
            <div style="
                font-size: 2rem;
                font-weight: 700;
                margin-top: 8px;
            ">
                {driver_probability * 100:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        if driver_risk_label == "High Risk":

            st.error(
                driver_status["message"]
            )

        else:

            st.success(
                driver_status["message"]
            )


    # =====================================================
    # BREAKDOWN RISK RESULT
    # =====================================================

    with breakdown_col:

        st.markdown("### 🔧 Vehicle Breakdown")

        st.metric(
            label=(
                f"{breakdown_status['icon']} "
                "Risk Status"
            ),
            value=breakdown_status["status"],
            border=True
        )

        st.caption(
            "High-Risk Probability"
        )

        st.progress(
            breakdown_probability
        )

        st.markdown(
            f"""
            <div style="
                font-size: 2rem;
                font-weight: 700;
                margin-top: 8px;
            ">
                {breakdown_probability * 100:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            f"AI Decision Threshold: "
            f"{threshold * 100:.0f}%"
        )

        if breakdown_risk_label == "High Risk":

            st.error(
                breakdown_status["message"]
            )

        else:

            st.success(
                breakdown_status["message"]
            )


    # =====================================================
    # OVERALL AI SAFETY SCORE
    # =====================================================

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # Calculate overall risk
    overall_risk = max(
        driver_probability,
        breakdown_probability
    )


    safety_score = max(
        0,
        100 - (overall_risk * 100)
    )


    # -----------------------------------------------------
    # OVERALL STATUS
    # -----------------------------------------------------

    if (
        driver_risk_label == "High Risk"
        or breakdown_risk_label == "High Risk"
    ):

        overall_status = "HIGH RISK"
        overall_icon = "🚨"

        overall_message = (
            "Potential safety concerns detected. "
            "Inspection and corrective action are recommended."
        )

    elif overall_risk >= 0.20:

        overall_status = "MODERATE RISK"
        overall_icon = "⚠️"

        overall_message = (
            "The vehicle is currently operating with "
            "moderate risk. Continue monitoring important "
            "safety parameters."
        )

    else:

        overall_status = "SAFE TO OPERATE"
        overall_icon = "🟢"

        overall_message = (
            "No immediate high-risk condition detected. "
            "The driver and vehicle safety indicators "
            "appear acceptable."
        )


    # =====================================================
    # OVERALL RESULT PANEL
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
            🛡️ Overall AI Safety Assessment
        </div>
        """,
        unsafe_allow_html=True
    )


    score_col, status_col = st.columns(
        [1, 2],
        gap="large"
    )


    with score_col:

        st.metric(
            label="🛡️ Overall Safety Score",
            value=f"{safety_score:.1f}%",
            border=True
        )


    with status_col:

        st.metric(
            label=(
                f"{overall_icon} "
                "Final Operating Status"
            ),
            value=overall_status,
            border=True
        )


    # =====================================================
    # FINAL AI RECOMMENDATION
    # =====================================================

    st.markdown("## 🤖 AI Recommendation")

    if overall_status == "HIGH RISK":

        st.error(
            overall_message
        )

    elif overall_status == "MODERATE RISK":

        st.warning(
            overall_message
        )

    else:

        st.info(
            overall_message
        )


# =========================================================
# INITIAL SCREEN MESSAGE
# =========================================================

else:

    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )

    st.info(
        "👆 Enter vehicle and driver parameters above, "
        "then click the AI analysis button to generate "
        "the safety assessment."
    )



 