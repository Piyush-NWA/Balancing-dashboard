import streamlit as st
import math
import pandas as pd
from PIL import Image

# =====================================================
# 🔁 CHANGE DATA MODE HERE ONLY
# =====================================================
DATA_MODE = "HARDCODED"   # Options: "HARDCODED" or "EXCEL"
# =====================================================

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Nautical Propeller Tool",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------
# CSS
# --------------------------------
st.markdown("""
<style>

header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 0rem !important;
    max-width: 820px;
}

.stApp {
    background-color: #B8D4D4;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #1F2937;
    margin-top: 25px;
    margin-bottom: 15px;
}

div[data-baseweb="select"] > div {
    height: 36px !important;
    min-height: 36px !important;
}

input {
    height: 36px !important;
}

input[aria-label="Radius X (mm)"],
input[aria-label="Radius Y (mm)"],
input[aria-label="Theta (radians)"],
input[aria-label="Theta (degrees)"],
input[aria-label="r (mm)"],
input[aria-label="2mm value"],
input[aria-label="2.5mm value"],
input[aria-label="3mm value"],
input[aria-label="3.5mm value"] {
    pointer-events: none !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #000000 !important;
}

div.stButton > button {
    background-color: #6FA8A8;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    height: 38px;
    width: 160px;
    border: none;
}

div.stButton > button:hover {
    background-color: #5c9c9c;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOGO
# --------------------------------
logo = Image.open("assets/logo with title.png")

col_logo1, col_logo2, col_logo3 = st.columns([1,2,2])
with col_logo2:
    st.image(logo, width=420)

# --------------------------------
# HARDCODED DATA
# --------------------------------
propeller_data = {
    14: {"radius_x": 100, "radius_y": 75},
    15: {"radius_x": 105, "radius_y": 75},
    16: {"radius_x": 105, "radius_y": 75},
    17: {"radius_x": 110, "radius_y": 75},
    18: {"radius_x": 125, "radius_y": 75},
    20: {"radius_x": 130, "radius_y": 75},
    22: {"radius_x": 130, "radius_y": 75},
    24: {"radius_x": 155, "radius_y": 75},
    26: {"radius_x": 165, "radius_y": 75},
    28: {"radius_x": 170, "radius_y": 75},
    30: {"radius_x": 190, "radius_y": 75},
    32: {"radius_x": 210, "radius_y": 75},
}

# --------------------------------
# DEFAULT DATA SOURCE
# --------------------------------
data_source = propeller_data

# --------------------------------
# LOAD EXCEL DATA (ONLY IF MODE = EXCEL)
# --------------------------------
if DATA_MODE == "EXCEL":
    try:
        df = pd.read_excel("propeller_data.xlsx")
        excel_data = {}
        for _, row in df.iterrows():
            size = int(row["PropellerSize"])
            excel_data[size] = {
                "radius_x": float(row["RadiusX_mm"]),
                "radius_y": float(row["RadiusY_mm"])
            }
        data_source = excel_data
        col_msg1, col_msg2 = st.columns([3, 2])
        with col_msg2:
            st.success("Excel data loaded successfully.")
    except Exception:
        st.error("Excel file not found or invalid format.")
        data_source = propeller_data

# --------------------------------
# PROPELLER DETAILS
# --------------------------------
st.markdown('<div class="section-title">Propeller Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    selected_size = st.selectbox("Propeller Size", list(data_source.keys()))

radius_x = data_source[selected_size]["radius_x"]
radius_y = data_source[selected_size]["radius_y"]

with col2:
    st.text_input("Radius X (mm)", value=radius_x)

with col3:
    st.text_input("Radius Y (mm)", value=radius_y)

st.divider()

# --------------------------------
# MASS INPUT
# --------------------------------
st.markdown('<div class="section-title">Mass Input</div>', unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    mass_x = st.text_input("Mass X")

with col5:
    mass_y = st.text_input("Mass Y")

# --------------------------------
# BUTTON
# --------------------------------
col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
with col_btn2:
    calculate = st.button("Calculate")

theta_rad = None
theta_deg = None
small_r = None

if calculate:
    if mass_x.strip() == "" or mass_y.strip() == "":
        st.error("Mass X and Mass Y are mandatory.")
    else:
        try:
            mx = float(mass_x)
            my = float(mass_y)
            denominator = mx * radius_x
            if denominator == 0:
                st.error("Mass X * Radius X cannot be zero.")
            else:
                theta_rad = math.atan((my * radius_y) / denominator)
                theta_deg = math.degrees(theta_rad)
                small_r = radius_x * math.tan(theta_rad)
        except Exception:
            st.error("Please enter valid numeric values.")

# --------------------------------
# RESULTS
# --------------------------------
if theta_rad is not None:
    st.divider()
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

    col6, col7, col8 = st.columns(3)

    with col6:
        st.text_input("Theta (radians)", value=round(theta_rad, 6))

    with col7:
        st.text_input("Theta (degrees)", value=round(theta_deg, 4))

    with col8:
        st.text_input("r (mm)", value=round(small_r, 4))

# --------------------------------
# WEIGHT DISTRIBUTION EXPANDER
# --------------------------------
st.markdown("""
<style>
details summary p {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #1F2937 !important;
}
</style>
""", unsafe_allow_html=True)

with st.expander("Mass X Distribution"):

    if theta_rad is not None:
        mx = float(mass_x)

        val_3_5mm = (0.8  * mx) / 1.8
        val_3mm   = (0.1  * mx) / 0.11
        val_2_5mm = (0.05 * mx) / 0.07
        val_2mm   = (0.05 * mx) / 0.04

        col_w1, col_w2, col_w3, col_w4 = st.columns(4)

        with col_w1:
            st.markdown("<p style='font-size:18px; font-weight:700;'>3.5mm</p>", unsafe_allow_html=True)
            st.text_input("3.5mm value", value=round(val_3_5mm, 4), label_visibility="collapsed")

        with col_w2:
            st.markdown("<p style='font-size:18px; font-weight:700;'>3mm</p>", unsafe_allow_html=True)
            st.text_input("3mm value", value=round(val_3mm, 4), label_visibility="collapsed")

        with col_w3:
            st.markdown("<p style='font-size:18px; font-weight:700;'>2.5mm</p>", unsafe_allow_html=True)
            st.text_input("2.5mm value", value=round(val_2_5mm, 4), label_visibility="collapsed")

        with col_w4:
            st.markdown("<p style='font-size:18px; font-weight:700;'>2mm</p>", unsafe_allow_html=True)
            st.text_input("2mm value", value=round(val_2mm, 4), label_visibility="collapsed")

    else:
        st.info("Calculate first to see weight distribution.")