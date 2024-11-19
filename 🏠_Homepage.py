import streamlit as st

# Set page configuration for wide layout
st.set_page_config(page_title="EOPD Tool House", layout="wide", page_icon="🏠",)

# Main Title and Subheading
st.title("🔧 EOPD Tool House")
st.subheader("Maximizing Performance with Precision Analytics and Data-Driven Advanced Tools: Your Toolkit for Every Performance Need")

# Page Description
st.write("## 💡What’s Inside")
st.write(
    "Welcome to the EOPD Tool House – your go-to platform for cutting-edge tools designed to streamline and enhance ship performance analysis. "
    "Here, you’ll find a range of powerful applications tailored to deliver in-depth insights, from fuel consumption optimization to weather impact "
    "assessments and route efficiency. Whether you’re a fleet manager or a performance analyst, our tools simplify complex data, empowering you to make "
    "informed decisions and drive operational excellence across every voyage."
)

# Tool Descriptions Heading
st.write("## 📖From Insight to Action: What Our Tools Deliver")


# Tool 2: sfoc calculator
with st.expander("⛽SFOC Calculator"):
    st.write("The SFOC (Specific Fuel Oil Consumption) Calculator is a powerful and user-friendly tool designed to assist in calculating SFOC, engine power, and fuel consumption based on specific input parameters.")


# Tool 3: Wind Direction Calculator
with st.expander("💨Wind Direction Calculator"):
    st.write(
	"The Wind Direction Calculator is a reliable and easy-to-use tool designed to help maritime professionals and enthusiasts determine accurate wind directions relative to true or magnetic north."
	"Whether you're planning voyages, assessing weather impact, or optimizing vessel routes, this tool ensures precise calculations to support informed decision-making."
	"With its intuitive interface, the Wind Direction Calculator allows users to input wind data, vessel heading, and reference points, delivering quick and reliable results."
	)

# Tool 1: Consumption Extrapolator with collapsible description
with st.expander("📈Cons Extrapolator"):
    st.write(
        "The Consumption Extrapolator is a powerful tool designed to estimate fuel consumption at various speeds beyond the known data points. "
        "Using advanced data regression and curve-fitting techniques, it allows users to input known speed and consumption data, then select their "
        "preferred fitting method—whether exponential or polynomial—to accurately project fuel consumption across a range of speeds."
    )


# Tool 4: disp normalization
with st.expander("📊Disp Normalization"):
    st.write(
        "Ship displacement normalization is a critical process in maritime performance analysis, ensuring accurate comparisons of vessel speed and fuel consumption across varying loads. By standardizing performance data"
        "to a reference displacement, this technique accounts for differences in laden and ballast conditions, enabling fair evaluations and insights into operational efficiency. Our approach combines advanced "
        "algorithms with hydrodynamic principles to deliver precise, actionable results for optimized vessel performance."
    )



# Tool 5: raw data
with st.expander("📋Boss_RwaData Cleanup"):
    st.write(
        "Boss_RawData Cleanup ensures that your raw data is transformed into a structured, usable format tailored to your specific requirements. By cleaning, filtering, and organizing the data, we eliminate inconsistencies"
        " and redundancies, enabling seamless analysis and accurate decision-making."

    )


# Tool 5: STW
with st.expander("🚤STW Calculator"):
    st.write(
        "This tool helps estimating Speed Through Water accurately with a given set of parameters"

    )





