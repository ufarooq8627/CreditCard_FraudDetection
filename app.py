import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os

# ──────────────────────────── Page Config ────────────────────────────
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────── Custom CSS ─────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* ── Hide default Streamlit elements ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Global ── */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* ── Hero Banner ── */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.25);
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.05); opacity: 1; }
    }

    .hero h1 {
        color: #fff;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }

    .hero p {
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem;
        margin-top: 0.6rem;
        position: relative;
        z-index: 1;
        font-weight: 300;
    }

    /* ── Section Headers ── */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Cards ── */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }

    /* ── Result Cards ── */
    .result-safe {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        border: 1px solid #10b981;
        box-shadow: 0 12px 40px rgba(5, 150, 105, 0.3);
    }

    .result-danger {
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        border: 1px solid #ef4444;
        box-shadow: 0 12px 40px rgba(220, 38, 38, 0.3);
        animation: danger-glow 2s ease-in-out infinite;
    }

    @keyframes danger-glow {
        0%, 100% { box-shadow: 0 12px 40px rgba(220, 38, 38, 0.3); }
        50% { box-shadow: 0 12px 60px rgba(220, 38, 38, 0.5); }
    }

    .result-safe h2, .result-danger h2 {
        color: #fff;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }

    .result-safe p, .result-danger p {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* ── Metric Tiles ── */
    .metric-tile {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s ease;
    }

    .metric-tile:hover {
        transform: translateY(-2px);
    }

    .metric-tile .label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin: 0;
    }

    .metric-tile .value {
        color: #fff;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0.4rem 0 0 0;
    }

    .metric-tile .value.fraud { color: #f87171; }
    .metric-tile .value.safe { color: #34d399; }

    /* ── Sidebar Styling ── */
    .sidebar-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        color: #e2e8f0;
        font-size: 0.85rem;
        line-height: 1.7;
    }

    .sidebar-card strong {
        color: #a78bfa;
    }

    .sidebar-card .title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .sidebar-badge {
        display: inline-block;
        background: #059669;
        color: white;
        font-size: 0.7rem;
        padding: 2px 8px;
        border-radius: 50px;
        font-weight: 600;
    }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        color: #475569;
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────── Load Model ─────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "fraud_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "models", "rbscaler.pkl")


@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


try:
    model, scaler = load_artifacts()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ──────────────────────────── Hero ───────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🛡️ FraudShield AI</h1>
    <p>Real-time credit card fraud detection powered by Neural Networks</p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error(f"❌ Could not load model: {model_error}")
    st.stop()

# ──────────────────────────── Sidebar ────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-title">⚙️ Input Mode</div>', unsafe_allow_html=True)
    input_mode = st.radio(
        "Choose how to input transaction data:",
        ["🎲 Random Transaction", "✏️ Manual Input", "📄 CSV Upload"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("""
    <div class="sidebar-card">
        <div class="title">📊 Model Details</div>
        <strong>Architecture:</strong> Neural Network (MLP)<br>
        <strong>Layers:</strong> 64 → 32 neurons<br>
        <strong>Features:</strong> 31 input features<br>
        <strong>Fraud Recall:</strong> <span class="sidebar-badge">1.00</span><br>
        <strong>F1 Score:</strong> 0.79
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="title">🏆 Model Leaderboard</div>
        Neural Network — <strong>F1: 0.79</strong> 🥇<br>
        Logistic Reg — F1: 0.08 🥈<br>
        XGBoost — F1: 0.01 🥉<br><br>
        <em style="color: #94a3b8;">Best model selected automatically</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="title">🔍 Key Fraud Indicators</div>
        <table style="width:100%; font-size:0.8rem; color:#e2e8f0;">
            <tr style="border-bottom:1px solid #334155;">
                <th style="text-align:left; padding:4px;">Feature</th>
                <th style="text-align:center; padding:4px;">🟢 Safe</th>
                <th style="text-align:center; padding:4px;">🔴 Fraud</th>
            </tr>
            <tr><td style="padding:4px;"><strong>V14</strong></td><td style="text-align:center; color:#34d399;">-1 to +1</td><td style="text-align:center; color:#f87171;">< -5</td></tr>
            <tr><td style="padding:4px;"><strong>V12</strong></td><td style="text-align:center; color:#34d399;">-1 to +1</td><td style="text-align:center; color:#f87171;">< -3</td></tr>
            <tr><td style="padding:4px;"><strong>V10</strong></td><td style="text-align:center; color:#34d399;">-1 to +1</td><td style="text-align:center; color:#f87171;">< -3</td></tr>
            <tr><td style="padding:4px;"><strong>V17</strong></td><td style="text-align:center; color:#34d399;">-1 to +1</td><td style="text-align:center; color:#f87171;">< -4</td></tr>
        </table>
        <br>
        <em style="color:#94a3b8;">💡 Try the fraud presets in Manual Input to see these in action!</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="title">📝 About</div>
        Trained on 284,807 transactions using SMOTE oversampling and Stratified K-Fold cross validation.
        The model catches <strong>99.99% of fraud</strong> during training.
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────── Feature Names ──────────────────────────
FEATURE_NAMES = (
    ["scaled_amount", "scaled_time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["extra_feature"]
)

# ──────────────────────────── Input Handling ──────────────────────────
input_data = None

if input_mode == "🎲 Random Transaction":
    st.markdown('<div class="section-title">🎲 Random Transaction Generator</div>', unsafe_allow_html=True)

    # Pool of real fraud transactions extracted from the dataset
    REAL_FRAUD_POOL = [
        [-0.3074, -0.9902, -2.3122, 1.952, -1.6099, 3.9979, -0.5222, -1.4265, -2.5374, 1.3917, -2.7701, -2.7723, 3.202, -2.8999, -0.5952, -4.2893, 0.3897, -1.1407, -2.8301, -0.0168, 0.417, 0.1269, 0.5172, -0.035, -0.4652, 0.3202, 0.0445, 0.1778, 0.2611, -0.1433, 0.0],
        [3.0452, -0.9426, -2.3033, 1.7592, -0.3597, 2.3302, -0.8216, -0.0758, 0.5623, -0.3991, -0.2383, -1.5254, 2.0329, -6.5601, 0.0229, -1.4701, -0.6988, -2.2822, -4.7818, -2.6157, -1.3344, -0.43, -0.2942, -0.9324, 0.1727, -0.0873, -0.1561, -0.5426, 0.0396, -0.153, 0.0],
        [0.517, -0.9129, -4.398, 1.3584, -2.5928, 2.6798, -1.1281, -1.7065, -3.4962, -0.2488, -0.2478, -4.8016, 4.8958, -10.9128, 0.1844, -6.7711, -0.0073, -7.3581, -12.5984, -5.1315, 0.3083, -0.1716, 0.5736, 0.177, -0.4362, -0.0535, 0.2524, -0.6575, -0.8271, 0.8496, 0.0],
        [-0.2934, -0.9066, 1.2342, 3.0197, -4.3046, 4.7328, 3.6242, -1.3577, 1.7134, -0.4964, -1.2829, -2.4475, 2.1013, -4.6096, 1.4644, -6.0793, -0.3392, 2.5819, 6.7394, 3.0425, -2.7219, 0.0091, -0.3791, -0.7042, -0.6568, -1.6327, 1.4889, 0.5668, -0.01, 0.1468, 0.0],
        [-0.2934, -0.9066, 0.0084, 4.1378, -6.2407, 6.6757, 0.7683, -3.3531, -1.6317, 0.1546, -2.7959, -6.1879, 5.6644, -9.8545, -0.3062, -10.6912, -0.6385, -2.042, -1.1291, 0.1165, -1.9347, 0.4884, 0.3645, -0.6081, -0.5395, 0.1289, 1.4885, 0.508, 0.7358, 0.5136, 0.0],
        [-0.2934, -0.9065, 0.0268, 4.1325, -6.5606, 6.3486, 1.3297, -2.5135, -1.6891, 0.3033, -3.1394, -6.0455, 6.7546, -8.9482, 0.7027, -10.7339, -1.3795, -1.639, -1.7464, 0.7767, -1.3274, 0.5877, 0.3705, -0.5768, -0.6696, -0.7599, 1.6051, 0.5407, 0.737, 0.4967, 0.0],
        [-0.2934, -0.9064, 0.3296, 3.7129, -5.7759, 6.0783, 1.6674, -2.4202, -0.8129, 0.1331, -2.2143, -5.1345, 4.5607, -8.8737, -0.7975, -9.1772, -0.257, -0.8717, 1.313, 0.7739, -2.3706, 0.2698, 0.1566, -0.6525, -0.5516, -0.7165, 1.4157, 0.5553, 0.5305, 0.4045, 0.0],
        [-0.2934, -0.9063, 0.3165, 3.8091, -5.6152, 6.0474, 1.554, -2.6514, -0.7466, 0.0556, -2.6787, -4.9595, 6.4391, -7.5201, 0.3864, -9.2523, -1.3652, -0.5024, 0.7844, 1.4943, -1.808, 0.3883, 0.2088, -0.5117, -0.5838, -0.2198, 1.4748, 0.4912, 0.5189, 0.4025, 0.0],
        [-0.2934, -0.9056, 0.7256, 2.3009, -5.33, 4.0077, -1.7304, -1.7322, -3.9686, 1.0637, -0.4861, -4.625, 5.5887, -7.1482, 1.6805, -6.2103, 0.4953, -3.5995, -4.8303, -0.6491, 2.2501, 0.5046, 0.5897, 0.1095, 0.601, -0.3647, -1.8431, 0.3519, 0.5945, 0.0994, 0.0],
        [-0.2934, -0.9049, 0.7027, 2.4264, -5.2345, 4.4167, -2.1708, -2.6676, -3.8781, 0.9113, -0.1662, -5.0092, 4.6757, -8.1672, 0.6386, -6.7633, 1.2969, -3.8118, -3.7541, -1.0492, 1.5542, 0.4227, 0.5512, -0.0098, 0.7217, 0.4732, -1.9593, 0.3195, 0.6005, 0.1293, 0.0],
    ]

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        transaction_type = st.selectbox(
            "Transaction Profile:",
            ["Normal (Random Values)", "Fraud (Real Fraud from Dataset)"],
        )
    with col2:
        seed = st.number_input("Random Seed:", min_value=0, max_value=9999, value=42)
    with col3:
        st.write("")  # spacing
        st.write("")
        predict_btn = st.button("🚀 Predict", use_container_width=True, type="primary")

    if predict_btn:
        np.random.seed(seed)
        if transaction_type == "Normal (Random Values)":
            input_data = np.random.randn(1, 31)
        else:
            # Pick a real fraud transaction based on the seed
            fraud_idx = seed % len(REAL_FRAUD_POOL)
            input_data = np.array(REAL_FRAUD_POOL[fraud_idx]).reshape(1, -1)
            st.caption(f"Using real fraud sample #{fraud_idx + 1} from the dataset")

elif input_mode == "✏️ Manual Input":
    st.markdown('<div class="section-title">✏️ Manual Feature Entry</div>', unsafe_allow_html=True)

    # ── Preset Definitions (real transactions from the dataset) ──
    PRESETS = {
        "🟢 Legitimate – Normal Purchase #1": {
            "desc": "A real legitimate transaction from the dataset (Row 0). Normal PCA features, nothing suspicious.",
            "values": [1.7833, -0.995, -1.3598, -0.0728, 2.5363, 1.3782, -0.3383, 0.4624, 0.2396, 0.0987,
                       0.3638, 0.0908, -0.5516, -0.6178, -0.9914, -0.3112, 1.4682, -0.4704, 0.208, 0.0258,
                       0.404, 0.2514, -0.0183, 0.2778, -0.1105, 0.0669, 0.1285, -0.1891, 0.1336, -0.0211, 0.0],
        },
        "🟢 Legitimate – Normal Purchase #2": {
            "desc": "Another real legitimate transaction (Row 1). Typical online purchase pattern.",
            "values": [-0.2698, -0.995, 1.1919, 0.2662, 0.1665, 0.4482, 0.06, -0.0824, -0.0788, 0.0851,
                       -0.2554, -0.167, 1.6127, 1.0652, 0.4891, -0.1438, 0.6356, 0.4639, -0.1148, -0.1834,
                       -0.1458, -0.0691, -0.2258, -0.6387, 0.1013, -0.3398, 0.1672, 0.1259, -0.009, 0.0147, 0.0],
        },
        "🔴 Fraud – Real Fraud Case #1": {
            "desc": "A real fraudulent transaction (Row 541). The model detects this with 100% confidence.",
            "values": [-0.3074, -0.9902, -2.3122, 1.952, -1.6099, 3.9979, -0.5222, -1.4265, -2.5374, 1.3917,
                       -2.7701, -2.7723, 3.202, -2.8999, -0.5952, -4.2893, 0.3897, -1.1407, -2.8301, -0.0168,
                       0.417, 0.1269, 0.5172, -0.035, -0.4652, 0.3202, 0.0445, 0.1778, 0.2611, -0.1433, 0.0],
        },
        "🔴 Fraud – Real Fraud Case #2": {
            "desc": "Another real fraud (Row 6108). Extreme V14 = -10.91, a key fraud indicator detected by the model.",
            "values": [0.517, -0.9129, -4.398, 1.3584, -2.5928, 2.6798, -1.1281, -1.7065, -3.4962, -0.2488,
                       -0.2478, -4.8016, 4.8958, -10.9128, 0.1844, -6.7711, -0.0073, -7.3581, -12.5984, -5.1315,
                       0.3083, -0.1716, 0.5736, 0.177, -0.4362, -0.0535, 0.2524, -0.6575, -0.8271, 0.8496, 0.0],
        },
        "⚙️ Custom – Enter Your Own Values": {
            "desc": "Manually enter all 31 feature values to test any pattern.",
            "values": [0.0] * 31,
        },
    }

    preset_choice = st.selectbox("📋 Select a Demo Preset:", list(PRESETS.keys()))
    preset = PRESETS[preset_choice]
    st.caption(preset["desc"])

    # Show the feature values in an expandable section
    with st.expander("📊 View / Edit Feature Values", expanded=("Custom" in preset_choice)):
        cols = st.columns(4)
        values = []
        for i, name in enumerate(FEATURE_NAMES):
            with cols[i % 4]:
                val = st.number_input(
                    name,
                    value=float(preset["values"][i]),
                    format="%.4f",
                    key=f"feat_{i}",
                )
                values.append(val)

    if st.button("🚀 Predict Transaction", use_container_width=True, type="primary"):
        input_data = np.array(values).reshape(1, -1)

elif input_mode == "📄 CSV Upload":
    st.markdown('<div class="section-title">📄 Batch Prediction via CSV</div>', unsafe_allow_html=True)
    st.caption("Upload a CSV with 31 columns matching the training features. Each row is one transaction.")

    uploaded_file = st.file_uploader("Drop your CSV here", type=["csv"], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded **{len(df_upload)}** transactions with **{df_upload.shape[1]}** features")
            st.dataframe(df_upload.head(), use_container_width=True)

            if df_upload.shape[1] != 31:
                st.warning(f"⚠️ Expected 31 columns, got {df_upload.shape[1]}.")

            if st.button("🚀 Predict All", use_container_width=True, type="primary"):
                input_data = df_upload.values
        except Exception as e:
            st.error(f"Error: {e}")

# ──────────────────────────── Prediction ─────────────────────────────
if input_data is not None:
    st.markdown("---")
    predictions = model.predict(input_data)
    probabilities = model.predict_proba(input_data)

    if len(predictions) == 1:
        pred = predictions[0]
        fraud_prob = probabilities[0][1]
        legit_prob = probabilities[0][0]

        if pred == 1:
            st.markdown("""
            <div class="result-danger">
                <h2>🚨 FRAUDULENT TRANSACTION DETECTED</h2>
                <p>This transaction has been flagged as potentially fraudulent. Immediate review recommended.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-safe">
                <h2>✅ TRANSACTION IS LEGITIMATE</h2>
                <p>This transaction appears to be safe. No suspicious activity detected.</p>
            </div>
            """, unsafe_allow_html=True)

        st.write("")  # spacing

        col1, col2, col3 = st.columns(3)
        with col1:
            color_class = "fraud" if fraud_prob > 0.5 else ""
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Fraud Probability</p>
                <p class="value {color_class}">{fraud_prob:.6f}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            color_class = "safe" if legit_prob > 0.5 else ""
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Legitimate Probability</p>
                <p class="value {color_class}">{legit_prob:.6f}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            verdict = "FRAUD" if pred == 1 else "SAFE"
            v_class = "fraud" if pred == 1 else "safe"
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Final Verdict</p>
                <p class="value {v_class}">{verdict}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        fraud_count = int(np.sum(predictions))
        legit_count = int(len(predictions) - fraud_count)
        fraud_pct = (fraud_count / len(predictions)) * 100

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Total Scanned</p>
                <p class="value">{len(predictions)}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Fraud Detected</p>
                <p class="value fraud">{fraud_count}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Legitimate</p>
                <p class="value safe">{legit_count}</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-tile">
                <p class="label">Fraud Rate</p>
                <p class="value fraud">{fraud_pct:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

        results_df = pd.DataFrame({
            "Transaction": range(1, len(predictions) + 1),
            "Status": ["🔴 Fraud" if p == 1 else "🟢 Safe" for p in predictions],
            "Fraud Prob": [f"{prob[1]:.6f}" for prob in probabilities],
            "Legit Prob": [f"{prob[0]:.6f}" for prob in probabilities],
        })
        st.markdown('<div class="section-title">📋 Detailed Results</div>', unsafe_allow_html=True)
        st.dataframe(results_df, use_container_width=True, hide_index=True)

# ──────────────────────────── Footer ─────────────────────────────────
st.markdown("""
<div class="app-footer">
    FraudShield AI &nbsp;•&nbsp; Neural Network (MLPClassifier) &nbsp;•&nbsp; Kaggle Credit Card Dataset &nbsp;•&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
