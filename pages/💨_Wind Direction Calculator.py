# C:\Users\paul\OneDrive - Oldendorff Carriers\Documents\Python Scripts\Wind
# streamlit run wind_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
import math

st.set_page_config(page_icon="💨",)

# Utility function to normalize angles
def normalize_angle(angle):
    return angle % 360

# Function to convert relative wind to true wind
def calculate_true_wind(relative_wind_speed, relative_wind_direction, ship_speed, ship_heading):
    # Convert angles from degrees to radians
    RWD_rad = math.radians(relative_wind_direction)
    SH_rad = math.radians(ship_heading)

    # Calculate x and y components of the relative wind vector
    RWx = relative_wind_speed * math.sin(RWD_rad)
    RWy = relative_wind_speed * math.cos(RWD_rad)

    # Calculate x and y components of the ship's motion vector
    SMx = ship_speed * math.sin(SH_rad)
    SMy = ship_speed * math.cos(SH_rad)

    # Calculate x and y components of the true wind vector
    TWx = RWx - SMx
    TWy = RWy - SMy

    # Calculate true wind speed
    true_wind_speed = math.sqrt(TWx ** 2 + TWy ** 2)

    # Calculate true wind direction (direction wind is coming from)
    true_wind_direction = normalize_angle(math.degrees(math.atan2(TWx, TWy)))

    return true_wind_speed, true_wind_direction

# Function to convert true wind to relative wind
def calculate_relative_wind(true_wind_speed, true_wind_direction, ship_speed, ship_heading):
    # Convert angles from degrees to radians
    TWD_rad = math.radians(true_wind_direction)
    SH_rad = math.radians(ship_heading)

    # Calculate x and y components of the true wind vector
    TWx = true_wind_speed * math.sin(TWD_rad)
    TWy = true_wind_speed * math.cos(TWD_rad)

    # Calculate x and y components of the ship's motion vector
    SMx = ship_speed * math.sin(SH_rad)
    SMy = ship_speed * math.cos(SH_rad)

    # Calculate x and y components of the relative wind vector
    RWx = TWx + SMx
    RWy = TWy + SMy

    # Calculate relative wind speed
    relative_wind_speed = math.sqrt(RWx**2 + RWy**2)

    # Calculate relative wind direction
    relative_wind_direction = normalize_angle(math.degrees(math.atan2(RWx, RWy)) - ship_heading)

    return relative_wind_speed, relative_wind_direction

# Streamlit UI
st.title("Wind Conversion: True Wind <-> Relative Wind")

col1, col2 = st.columns([1, 2])

with col1:
    # Select conversion type
    conversion_type = st.selectbox("Select Conversion Type:", ["Relative Wind to True Wind", "True Wind to Relative Wind"], key="conversion_type")

    # Inputs
    heading = st.slider("Heading (deg)", 0, 360, step=5, key="heading")
    stw = st.slider("Ship's Speed (STW) (kts)", 6, 30, step=1, key="stw")
    wind_speed_unit = st.radio("Wind Speed Unit:", ("knots", "m/sec"), index=0, key="wind_speed_unit")

    if conversion_type == "Relative Wind to True Wind":
        rel_wind_dir = st.slider("Relative Wind Direction (-180 to 180 deg)", -180, 180, step=5, key="rel_wind_dir")
        rel_wind_speed = st.slider("Relative Wind Speed", 0, 60, step=5, key="rel_wind_speed")
        if wind_speed_unit == "m/sec":
            rel_wind_speed *= 1.94384  # Convert to knots

        # Calculate true wind
        true_wind_speed, true_wind_dir = calculate_true_wind(rel_wind_speed, rel_wind_dir, stw, heading)
        if wind_speed_unit == "m/sec":
            true_wind_speed /= 1.94384  # Convert back to m/sec

        st.write(f"**True Wind Direction: {int(true_wind_dir)} deg**")
        st.write(f"**True Wind Speed: {int(true_wind_speed)} kts**")
        wind_speed = max(rel_wind_speed, stw, true_wind_speed) + 5
        plot_title = "Relative Wind to True Wind"
        plot_vectors = [(heading, stw, 'r', 'Ship Heading & STW')]
        true_wind_arrow = (true_wind_dir, wind_speed, true_wind_speed)

    else:
        true_wind_dir = st.slider("True Wind Direction (0 to 360 deg)", 0, 360, step=5, key="true_wind_dir")
        true_wind_speed = st.slider("True Wind Speed", 0, 60, step=5, key="true_wind_speed")
        if wind_speed_unit == "m/sec":
            true_wind_speed *= 1.94384  # Convert to knots

        # Calculate relative wind
        rel_wind_speed, rel_wind_dir = calculate_relative_wind(true_wind_speed, true_wind_dir, stw, heading)
        if wind_speed_unit == "m/sec":
            rel_wind_speed /= 1.94384  # Convert back to m/sec

        st.write(f"**Relative Wind Direction: {int(rel_wind_dir)} deg**")
        st.write(f"**Relative Wind Speed: {int(rel_wind_speed)} kts**")
        wind_speed = max(rel_wind_speed, stw, true_wind_speed) + 5
        plot_title = "True Wind to Relative Wind"
        plot_vectors = [(heading, stw, 'r', 'Ship Heading & STW')]
        true_wind_arrow = (true_wind_dir, wind_speed, true_wind_speed)

# Plotting polar diagram
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': 'polar'})  # Reduce the size by 30%
ax.set_title(plot_title, pad=20)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

# Plot concentric circles
for r in range(0, int(wind_speed) + 5, 5):
    ax.add_patch(Circle((0, 0), r, transform=ax.transData._b, color="grey", alpha=0.2, fill=False))

# Plot vectors
for angle, speed, color, label in plot_vectors:
    angle_rad = np.radians(angle)
    ax.plot([0, angle_rad], [0, speed], color=color, label=label)

# Plot true wind as an arrow from the periphery towards the center
true_wind_angle_rad = np.radians(true_wind_arrow[0])
arrow_length = 5  # Fixed length for the arrow
start_radius = wind_speed
end_radius = start_radius - arrow_length
ax.annotate('', xy=(true_wind_angle_rad, end_radius), xytext=(true_wind_angle_rad, start_radius),
            arrowprops=dict(facecolor='blue', edgecolor='blue', arrowstyle='-|>', lw=2))
ax.text(true_wind_angle_rad, start_radius + 1, f'{int(true_wind_arrow[2])} kts', color='blue', fontsize=10, fontweight='bold', ha='left', va='center')

ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25))

with col2:
    st.pyplot(fig)
