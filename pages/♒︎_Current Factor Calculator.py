import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import radians, degrees, sin, cos, atan2, sqrt

# Helper function to calculate Speed Through Water (STW) and heading
def calculate_stw(cog, sog, current_dir, current_speed):
    # Convert angles to radians
    cog_rad = radians(cog)
    current_dir_rad = radians(current_dir)

    # Resolve SOG and current speed into x and y components
    sog_x = sog * cos(cog_rad)
    sog_y = sog * sin(cog_rad)
    current_x = current_speed * cos(current_dir_rad)
    current_y = current_speed * sin(current_dir_rad)

    # Calculate STW components
    stw_x = sog_x - current_x
    stw_y = sog_y - current_y

    # Calculate STW and heading
    stw = sqrt(stw_x**2 + stw_y**2)
    heading = degrees(atan2(stw_y, stw_x)) % 360

    return stw, heading, sog_x, sog_y, current_x, current_y

# Helper function to calculate Speed Over Ground (SOG) and Course Over Ground (COG)
def calculate_sog(stw, heading, current_dir, current_speed):
    # Convert angles to radians
    heading_rad = radians(heading)
    current_dir_rad = radians(current_dir)

    # Resolve STW and current speed into x and y components
    stw_x = stw * cos(heading_rad)
    stw_y = stw * sin(heading_rad)
    current_x = current_speed * cos(current_dir_rad)
    current_y = current_speed * sin(current_dir_rad)

    # Calculate SOG components
    sog_x = stw_x + current_x
    sog_y = stw_y + current_y

    # Calculate SOG and COG
    sog = sqrt(sog_x**2 + sog_y**2)
    cog = degrees(atan2(sog_y, sog_x)) % 360

    return sog, cog

# Helper function to calculate Current Direction and Speed
def calculate_current(sog, cog, stw, heading):
    # Convert angles to radians
    cog_rad = radians(cog)
    heading_rad = radians(heading)

    # Resolve SOG and STW into x and y components
    sog_x = sog * cos(cog_rad)
    sog_y = sog * sin(cog_rad)
    stw_x = stw * cos(heading_rad)
    stw_y = stw * sin(heading_rad)

    # Calculate current components
    current_x = sog_x - stw_x
    current_y = sog_y - stw_y

    # Calculate current speed and direction
    current_speed = sqrt(current_x**2 + current_y**2)
    current_dir = degrees(atan2(current_y, current_x)) % 360

    return current_dir, current_speed

# Streamlit UI
def main():
    st.title("Navigator's App - Wind & Current calculator ")

    # Selection of calculation type
    calculation_type = st.radio("Select Calculation Type:", [
        "Calculate Heading & Speed Through Water (STW)",
        "Calculate Course Over Ground (COG) & Speed Over Ground (SOG)",
        "Calculate Current Direction & Speed"
    ])

    # Layout
    left_col, right_col = st.columns([1, 3])

    if calculation_type == "Calculate Heading & Speed Through Water (STW)":
        with left_col:
            # Inputs
            cog = st.slider("Ship's Course Over Ground (COG) [deg]", 0, 360, step=5)
            sog = st.slider("Speed Over Ground (SOG) [kts]", 6.0, 30.0, step=0.5)
            current_dir = st.slider("Current Direction [deg]", 0, 360, step=5)
            current_speed = st.slider("Current Speed [kts]", 0.0, 5.0, step=0.25)

        # Calculate STW, heading, and current factor
        stw, heading, sog_x, sog_y, current_x, current_y = calculate_stw(cog, sog, current_dir, current_speed)
        current_factor = sog - stw

        with right_col:
            # Plotting polar diagram
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3.94, 3.94))
            max_radius = max(sog, stw) + 1

            # Plot concentric circles
            ax.set_rmax(max_radius)
            ax.set_rticks(np.arange(0, max_radius, 2))
            ax.tick_params(axis='y', labelsize='small')  # Reduce font size of the speeds by 50%  # Radial ticks every 2 kts
            ax.grid(True)
            
            # Plot vectors
            # Plot AB (Heading & STW)
            ax.plot([radians(heading), radians(heading)], [0, stw], label='Heading & STW', color='green')
            # Plot AC (COG & SOG)
            ax.plot([radians(cog), radians(cog)], [0, sog], label='COG & SOG', color='blue', linestyle='--')
            # Plot BC (Current direction & Current speed) starting from B to C
            bx_angle = heading
            bx_radius = stw
            cx_angle = cog
            cx_radius = sog
            ax.annotate('', xy=(radians(cx_angle), cx_radius), xytext=(radians(bx_angle), bx_radius), arrowprops=dict(arrowstyle='->', color='red'))
            # Plot BC (Current direction & Current speed) explicitly for legend
            ax.plot([radians(bx_angle), radians(cx_angle)], [bx_radius, cx_radius], color='red', linestyle=':', label='Current Direction & Speed - Red arrow')

            # Formatting polar plot
            ax.set_theta_zero_location('N')  # North at top
            ax.set_theta_direction(-1)  # Clockwise direction
            
            # Move legend below polar plot
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize='x-small')

            # Show plot
            st.pyplot(fig)

            # Display results below the polar plot
            st.metric("Ship's Heading & Speed Through Water (STW)", f"{heading:.0f} deg / {stw:.1f} kts")
            current_factor_color = f"<span style='font-size: 2.25em; font-weight: bold; color: {'green' if current_factor > 0 else 'red'};'>{current_factor:.1f} kts</span>"
            st.markdown(f"Current Factor: {current_factor_color}", unsafe_allow_html=True)

    elif calculation_type == "Calculate Course Over Ground (COG) & Speed Over Ground (SOG)":
        with left_col:
            # Inputs
            heading = st.slider("Ship's Heading [deg]", 0, 360, step=5)
            stw = st.slider("Speed Through Water (STW) [kts]", 0.0, 30.0, step=0.5)
            current_dir = st.slider("Current Direction [deg]", 0, 360, step=5)
            current_speed = st.slider("Current Speed [kts]", 0.0, 5.0, step=0.25)

        # Calculate SOG and COG
        sog, cog = calculate_sog(stw, heading, current_dir, current_speed)
        current_factor = sog - stw

        with right_col:
            # Plotting polar diagram
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3.94, 3.94))
            max_radius = max(sog, stw) + 1

            # Plot concentric circles
            ax.set_rmax(max_radius)
            ax.set_rticks(np.arange(0, max_radius, 2))
            ax.tick_params(axis='y', labelsize='small')  # Reduce font size of the speeds by 50%  # Radial ticks every 2 kts
            ax.grid(True)
            
            # Plot vectors
            # Plot AB (Heading & STW)
            ax.plot([radians(heading), radians(heading)], [0, stw], label='Heading & STW', color='green')
            # Plot AC (COG & SOG)
            ax.plot([radians(cog), radians(cog)], [0, sog], label='COG & SOG', color='blue', linestyle='--')
            # Plot BC (Current direction & Current speed) starting from B to C
            bx_angle = heading
            bx_radius = stw
            cx_angle = cog
            cx_radius = sog
            ax.annotate('', xy=(radians(cx_angle), cx_radius), xytext=(radians(bx_angle), bx_radius), arrowprops=dict(arrowstyle='->', color='red'))
            # Plot BC (Current direction & Current speed) explicitly for legend
            ax.plot([radians(bx_angle), radians(cx_angle)], [bx_radius, cx_radius], color='red', linestyle=':', label='Current Direction & Speed - Red arrow')

            # Formatting polar plot
            ax.set_theta_zero_location('N')  # North at top
            ax.set_theta_direction(-1)  # Clockwise direction
            
            # Move legend below polar plot
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize='x-small')

            # Show plot
            st.pyplot(fig)

            # Display results below the polar plot
            st.metric("Course Over Ground (COG) & Speed Over Ground (SOG)", f"{cog:.0f} deg / {sog:.1f} kts")
            current_factor_color = f"<span style='font-size: 2.25em; font-weight: bold; color: {'green' if current_factor > 0 else 'red'};'>{current_factor:.1f} kts</span>"
            st.markdown(f"Current Factor: {current_factor_color}", unsafe_allow_html=True)

    elif calculation_type == "Calculate Current Direction & Speed":
        with left_col:
            # Inputs
            cog = st.slider("Course Over Ground (COG) [deg]", 0, 360, step=5)
            sog = st.slider("Speed Over Ground (SOG) [kts]", 6.0, 30.0, step=0.5)
            heading = st.slider("Ship's Heading [deg]", 0, 360, step=5)
            stw = st.slider("Speed Through Water (STW) [kts]", 0.0, 30.0, step=0.5)

        # Calculate Current Direction and Speed
        current_dir, current_speed = calculate_current(sog, cog, stw, heading)
        current_factor = sog - stw

        with right_col:
            # Plotting polar diagram
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3.94, 3.94))
            max_radius = max(sog, stw) + 1

            # Plot concentric circles
            ax.set_rmax(max_radius)
            ax.set_rticks(np.arange(0, max_radius, 2))
            ax.tick_params(axis='y', labelsize='small')  # Reduce font size of the speeds by 50%  # Radial ticks every 2 kts
            ax.grid(True)
            
            # Plot vectors
            # Plot AB (Heading & STW)
            ax.plot([radians(heading), radians(heading)], [0, stw], label='Heading & STW', color='green')
            # Plot AC (COG & SOG)
            ax.plot([radians(cog), radians(cog)], [0, sog], label='COG & SOG', color='blue', linestyle='--')
            # Plot BC (Current direction & Current speed) starting from B to C
            bx_angle = heading
            bx_radius = stw
            cx_angle = cog
            cx_radius = sog
            ax.annotate('', xy=(radians(cx_angle), cx_radius), xytext=(radians(bx_angle), bx_radius), arrowprops=dict(arrowstyle='->', color='red'))
            # Plot BC (Current direction & Current speed) explicitly for legend
            ax.plot([radians(bx_angle), radians(cx_angle)], [bx_radius, cx_radius], color='red', linestyle=':', label='Current Direction & Speed - Red arrow')

            # Formatting polar plot
            ax.set_theta_zero_location('N')  # North at top
            ax.set_theta_direction(-1)  # Clockwise direction
            
            # Move legend below polar plot
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize='x-small')

            # Show plot
            st.pyplot(fig)

            # Display results below the polar plot
            st.metric("Current Direction & Speed", f"{current_dir:.0f} deg / {current_speed:.1f} kts")
            current_factor_color = f"<span style='font-size: 2.25em; font-weight: bold; color: {'green' if current_factor > 0 else 'red'};'>{current_factor:.1f} kts</span>"
            st.markdown(f"Current Factor: {current_factor_color}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()