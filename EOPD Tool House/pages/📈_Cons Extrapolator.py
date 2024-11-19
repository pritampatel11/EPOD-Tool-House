import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set wide layout for the Streamlit app
st.set_page_config(layout="wide", page_icon="📈",)

# Initialize session state for data storage
if 'speed_me_cons' not in st.session_state:
    st.session_state['speed_me_cons'] = pd.DataFrame({
        "Speed (kn)": [10.5, 11, 11.5, 12, 12.5, 13],
        "ME Cons (MT/24Hr)": [20.5, 22.4, 24.5, 26.8, 29.3, 32]
    })
if 'fit_type' not in st.session_state:
    st.session_state['fit_type'] = 'Exponential'

# Input data in tabular format
st.write("## Consumption Extrapolator")

# Data editor for entering speed and ME consumption values
st.write("### Enter Speed and ME Cons Data")
data_df = st.data_editor(st.session_state['speed_me_cons'], num_rows="dynamic")

# Update session state with new data
if st.button("Submit Data"):
    st.session_state['speed_me_cons'] = data_df

# Extract speed and ME Cons from the updated table
speed = st.session_state['speed_me_cons']["Speed (kn)"].values
me_cons = st.session_state['speed_me_cons']["ME Cons (MT/24Hr)"].values

# Side-by-side layout for input speed slider and fit type dropdown
col1, col2 = st.columns(2)
with col1:
    input_speed = st.slider("Input Speed (knots):", min_value=8.0, max_value=15.0, value=11.5, step=0.1)
with col2:
    fit_type = st.selectbox("Select Fit Type:", ["Exponential", "Polynomial"])

# If polynomial fit is selected, show degree selection slider
if fit_type == "Polynomial":
    degree = st.slider("Select Degree of Polynomial:", 1, 5, 2)

# Calculate ME Consumption based on selected fit type
if fit_type == "Exponential":
    b = np.polyfit(speed, np.log(me_cons), 1)[0]
    a = np.exp(np.polyfit(speed, np.log(me_cons), 1)[1])
    calculated_me_cons = a * np.exp(b * input_speed)
    fitted_me_cons = a * np.exp(b * speed)
    formula = f"ME Cons = {a:.4f} * exp({b:.4f} * Speed)"
else:
    coeffs = np.polyfit(speed, me_cons, degree)
    poly_model = np.poly1d(coeffs)
    calculated_me_cons = poly_model(input_speed)
    fitted_me_cons = poly_model(speed)
    formula = f"ME Cons = {' + '.join([f'{c:.4f}*Speed^{i}' for i, c in enumerate(coeffs[::-1])])}"

# Display calculated ME Consumption for the input speed
st.write(f"### Calculated ME Cons for {input_speed} kn: {calculated_me_cons:.2f} MT/24Hr")
st.write(f"Fitted Model: {formula}")

# Create side-by-side columns for plot and table
col3, col4 = st.columns(2)

# Plot the data and fitted model in the first column
with col3:
    fig, ax = plt.subplots()
    ax.scatter(speed, me_cons, color="blue", label="Observed Data")
    ax.plot(speed, fitted_me_cons, color="red", label="Fitted Model")
    ax.scatter(input_speed, calculated_me_cons, color="green", label=f"Input Speed: {input_speed} kn", s=100, marker='x')
    ax.set_xlabel("Speed (kn)")
    ax.set_ylabel("ME Cons (MT/24Hr)")
    ax.legend()
    st.pyplot(fig)

# Output table for ME Cons over a speed range (8 to 15 in 0.5 steps) in the second column
speed_range = np.arange(8, 15.5, 0.5)
if fit_type == "Exponential":
    me_cons_range = a * np.exp(b * speed_range)
else:
    me_cons_range = poly_model(speed_range)

# Format table values to one decimal place and remove index
output_df = pd.DataFrame({"Speed (kn)": np.round(speed_range, 1), "ME Cons (MT/24Hr)": np.round(me_cons_range, 1)})

# Display the table in the second column without the index
with col4:
    st.write("### ME Consumption Table for Speed Range 8-15 kn")
    st.table(output_df)
