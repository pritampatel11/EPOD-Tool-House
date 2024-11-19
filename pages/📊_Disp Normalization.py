import streamlit as st
import numpy as np

st.set_page_config(page_icon="📊",)

def main():
    st.title("Displacement Normalization Calculator")

    st.markdown(
        """
        <style>
        .grey-box {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
        }
        .bold {
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="grey-box">', unsafe_allow_html=True)
        current_displacement = st.number_input(
            "**Current Displacement (mts)**",
            min_value=10000,
            max_value=300000,
            value=50000,
            step=1
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="grey-box">', unsafe_allow_html=True)
        new_displacement = st.number_input(
            "**New Displacement (mts)**",
            min_value=10000,
            max_value=300000,
            value=60000,
            step=1
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        option = st.radio("**Total Cons / ME cons**", ("Total Consumption", "ME Consumption"))

    if option == "Total Consumption":
        with col2:
            st.markdown('<div class="grey-box">', unsafe_allow_html=True)
            total_cons = st.number_input(
                "**Total Consumption (mts/day)**",
                min_value=10.0,
                max_value=70.0,
                value=30.0,
                step=0.1
            )
            ae_cons = st.number_input(
                "**AE Consumption (mts/day)**",
                min_value=1.0,
                max_value=9.0,
                value=2.0,
                step=0.1
            )
            st.markdown('</div>', unsafe_allow_html=True)
            me_cons = total_cons - ae_cons
    else:
        with col2:
            st.markdown('<div class="grey-box">', unsafe_allow_html=True)
            me_cons = st.number_input(
                "**ME Consumption (mts/day)**",
                min_value=10.0,
                max_value=70.0,
                value=30.0,
                step=0.1
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        st.markdown('<div class="grey-box">', unsafe_allow_html=True)
        n = st.slider(
            "**Admiralty Coefficient (n)**",
            min_value=0.20,
            max_value=0.99,
            value=0.66,
            step=0.01
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Calculations
    new_me_cons = me_cons * (new_displacement / current_displacement) ** n
    percent_change = ((new_me_cons - me_cons) / me_cons) * 100

    # Outputs
    st.markdown(
        f"<h3 style='color: blue; font-weight: bold;'>New ME Consumption: {new_me_cons:.1f} mts/day</h3>",
        unsafe_allow_html=True
    )

    if option == "Total Consumption":
        new_total_cons = new_me_cons + ae_cons
        st.markdown(
            f"<h3 style='color: blue; font-weight: bold;'>New Total Consumption: {new_total_cons:.1f} mts/day</h3>",
            unsafe_allow_html=True
        )

    if percent_change > 0:
        st.markdown(
            f"<h3 style='color: red; font-weight: bold;'>% Change in ME Consumption: {percent_change:.1f}% &#9650;</h3>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<h3 style='color: green; font-weight: bold;'>% Change in ME Consumption: {percent_change:.1f}% &#9660;</h3>",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()

