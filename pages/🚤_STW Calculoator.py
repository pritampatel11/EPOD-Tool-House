import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_icon="🚤",)

def calculate_speed_through_water(ship_heading, sog, current_speed, current_direction):
    # Convert headings and directions from degrees to radians
    ship_heading_rad = math.radians(ship_heading)
    current_direction_rad = math.radians(current_direction)
    
    # Resolve the ship's velocity into components
    ship_velocity_x = sog * math.sin(ship_heading_rad)
    ship_velocity_y = sog * math.cos(ship_heading_rad)

    # Resolve the current's velocity into components
    current_velocity_x = current_speed * math.sin(current_direction_rad)
    current_velocity_y = current_speed * math.cos(current_direction_rad)

    # Calculate the resulting velocity components
    resultant_velocity_x = ship_velocity_x - current_velocity_x
    resultant_velocity_y = ship_velocity_y - current_velocity_y

    # Calculate speed through water
    stw = math.sqrt(resultant_velocity_x**2 + resultant_velocity_y**2)
    
    # Calculate ship's course
    course_rad = math.atan2(resultant_velocity_x, resultant_velocity_y)
    course_deg = math.degrees(course_rad)
    if course_deg < 0:
        course_deg += 360
    
    return stw, course_deg, resultant_velocity_x, resultant_velocity_y

def plot_polar_diagram(ship_heading, sog, current_speed, current_direction, stw, course):
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    # Convert degrees to radians for plotting
    ship_heading_rad = math.radians(ship_heading)
    current_direction_rad = math.radians(current_direction)
    course_rad = math.radians(course)

    # Plot ship's heading
    ax.quiver(ship_heading_rad, 0, 0, sog, angles='xy', scale_units='xy', scale=1, color='b', label='Ship Heading & SOG')
    
    # Plot current direction
    ax.quiver(current_direction_rad, 0, 0, current_speed, angles='xy', scale_units='xy', scale=1, color='r', label='Current Direction & Speed')
    
    # Plot speed through water
    ax.quiver(course_rad, 0, 0, stw, angles='xy', scale_units='xy', scale=1, color='g', label='Speed Through Water & Course')

    # Add legend and labels
    ax.set_title('Ship Speed and Current Diagram')
    ax.legend(loc='upper right')

    st.pyplot(fig)

def main():
    st.title("Ship Speed Through Water Calculator")
    
    # User inputs
    ship_heading = st.slider("Ship's Heading (degrees)", 0, 360, 0, step=12)
    sog = st.slider("Ship's Speed Over Ground (knots)", 0.0, 30.0, 0.0, step=0.25)
    current_speed = st.slider("Current Speed (knots)", 0.0, 10.0, 0.0, step=0.25)
    current_direction = st.slider("Current Direction (degrees)", 0, 360, 0, step=12)
    
    if st.button("Calculate Speed Through Water"):
        stw, course, resultant_velocity_x, resultant_velocity_y = calculate_speed_through_water(ship_heading, sog, current_speed, current_direction)
        st.success(f"The Speed Through Water is: {stw:.2f} knots")
        st.success(f"The Ship's Course is: {course:.2f} degrees")
        
        # Plot visualization
        plot_polar_diagram(ship_heading, sog, current_speed, current_direction, stw, course)

if __name__ == "__main__":
    main()