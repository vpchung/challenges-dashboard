import streamlit as st


def footer_html() -> str:
    """HTML for a basic footer."""
    return """
        <div class='footer'>
            © 2025, Challenges & Benchmarking <br/>
            <i>Powered by Sage Bionetworks</i></p>
        </div>
    """

# Configure the layout of the Streamlit app page
st.set_page_config(
    layout="wide",
    page_title="Challenges on Synapse",
    page_icon=":chart_with_upwards_trend:",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling (Optional)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/metrics.py", title="Home"),
    st.Page("pages/directory_list.py", title="Directory List"),
    st.Page("pages/download_counts.py", title="Data Download Counts")
])

pg.run()

st.markdown(footer_html(), unsafe_allow_html=True)
