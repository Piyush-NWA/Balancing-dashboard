import streamlit as st
import math
from PIL import Image

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

/* Section title */
.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #1F2937;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* Match selectbox height */
div[data-baseweb="select"] > div {
    height: 36px !important;
    min-height: 36px !important;
}

/* Match text input height */
input {
    height: 36px !important;
}

/* Make radius non-editable */
input[aria-label="Radius X"],
input[aria-label="Radius Y"] {
    pointer-events: none;
    background-color: #FFFFFF !important;
    color: #000000 !important;
    opacity: 1 !important;
}

/* Button */
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

logo = Image.open("assets/logo with title.png")

col_logo1, col_logo2, col_logo3 = st.columns([1,2,3])
with col_logo2:
    st.image(logo, width=420)

# --------------------------------
# HARDCODED RADIUS VALUES
# --------------------------------
propeller_data = {
    14: {"radius_x": 7.10, "radius_y": 6.52},
    15: {"radius_x": 7.48, "radius_y": 6.91},
    16: {"radius_x": 8.03, "radius_y": 7.52},
    17: {"radius_x": 8.42, "radius_y": 7.88},
    18: {"radius_x": 8.95, "radius_y": 8.31},
    19: {"radius_x": 9.37, "radius_y": 8.76},
    20: {"radius_x": 9.92, "radius_y": 9.11},
    21: {"radius_x": 10.36, "radius_y": 9.58},
    22: {"radius_x": 10.87, "radius_y": 10.02},
    23: {"radius_x": 11.28, "radius_y": 10.44},
    24: {"radius_x": 11.75, "radius_y": 10.89},
    25: {"radius_x": 12.19, "radius_y": 11.36},
    26: {"radius_x": 12.63, "radius_y": 11.84},
    27: {"radius_x": 13.08, "radius_y": 12.21},
    28: {"radius_x": 13.54, "radius_y": 12.73},
}

# --------------------------------
# PROPELLER DETAILS
# --------------------------------
st.markdown('<div class="section-title">Propeller Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    selected_size = st.selectbox(
        "Propeller Size",
        list(propeller_data.keys())
    )

radius_x = propeller_data[selected_size]["radius_x"]
radius_y = propeller_data[selected_size]["radius_y"]

with col2:
    st.text_input("Radius X", value=radius_x)

with col3:
    st.text_input("Radius Y", value=radius_y)

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

        except:
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
        st.text_input("r", value=round(small_r, 4))