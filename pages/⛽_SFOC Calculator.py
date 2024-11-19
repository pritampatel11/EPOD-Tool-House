import streamlit as st

st.set_page_config(page_icon="⛽",)

def calculate_cons_day(sfoc, power):
    return sfoc * power / 1000000 * 24

def calculate_sfoc(cons_day, power):
    return cons_day * 1000000 / 24 / power

def calculate_power(cons_day, sfoc):
    return cons_day * 1000000 / 24 / sfoc

st.title('SFOC Calculation App')
st.write('Select an option to perform the respective calculation.')

# User option selection
option = st.radio('Select Calculation', ('Calculate Cons/Day', 'Calculate SFOC', 'Calculate Power'))

if option == 'Calculate Cons/Day':
    st.header('Calculate Cons/Day')
    sfoc = st.number_input('Enter SFOC (kg/kWh):', min_value=0.0, format='%f')
    power = st.number_input('Enter Power (kWh):', min_value=0.0, format='%f')
    if st.button('Calculate'):
        result = calculate_cons_day(sfoc, power)
        st.write(f'Daily Fuel Consumption: {result:.1f} mts/day')

elif option == 'Calculate SFOC':
    st.header('Calculate SFOC')
    cons_day = st.number_input('Enter Cons/Day (mts/day):', min_value=0.0, format='%f')
    power = st.number_input('Enter Power (kWh):', min_value=0.0, format='%f')
    if st.button('Calculate'):
        result = calculate_sfoc(cons_day, power)
        st.write(f'SFOC: {result:.1f} kg/kWh')

elif option == 'Calculate Power':
    st.header('Calculate Power')
    cons_day = st.number_input('Enter Cons/Day (mts/day):', min_value=0.0, format='%f')
    sfoc = st.number_input('Enter SFOC (kg/kWh):', min_value=0.0, format='%f')
    if st.button('Calculate'):
        result = calculate_power(cons_day, sfoc)
        st.write(f'Power: {result:.1f} kWh')