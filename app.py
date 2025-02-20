import streamlit as st

from toolkit.queries import query_challenges, query_data_download_counts
from toolkit.utils import force_display_all_rows, get_data_from_snowflake, human_format

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

# Add user interface elements to sidebar
PLOT_OPTIONS = ["Metrics", "Directory", "Data Downloads"]
SELECTED_OPTION = st.sidebar.selectbox("Dashboard Page", PLOT_OPTIONS)


def footer_html() -> str:
    """HTML for a basic footer."""
    return """
        <div class='footer'>
            © 2025, Challenges & Benchmarking <br/>
            <i>Powered by Sage Bionetworks</i></p>
        </div>
    """


def app(selected_option):
    st.markdown("# Challenges on Synapse")

    # 1. Retrieve the data using your queries in queries.py
    # -------------------------------------------------------------------------
    challenges = get_data_from_snowflake(query_challenges())

    # Create new column for hyperlinks
    challenges["Link"] = "https://www.synapse.org/Synapse:syn" + challenges[
        "PROJECT_ID"
    ].astype(str)

    # Create new column for challenge year (assuming YEAR(creation_date) is the start year)
    challenges["Year"] = challenges["DATE"].astype(str).str.split("-", expand=True)[0]
    challenges_by_year = (
        challenges.groupby("Year").size().reset_index(name="Number of Challenges")
    )

    # 2. Get general metrics and delta numbers
    num_challenges = len(challenges)
    delta_challenges = challenges_by_year["Number of Challenges"].diff().iloc[-1]

    delta_participants = 8_100
    delta_submissions = 65_420

    # 3. Display the data
    # -------------------------------------------------------------------------
    st.markdown(f"#### {selected_option}")

    if selected_option == "Metrics":
        col1, col2, col3 = st.columns(3)
        col1.metric("Challenges", num_challenges, int(delta_challenges))
        col2.metric("Participants", human_format(delta_participants), "5%")
        col3.metric("Submissions", human_format(delta_submissions))

        st.markdown("#### Challenges By Year")
        st.dataframe(
            challenges_by_year.sort_values("Year", ascending=False),
            hide_index=True,
            use_container_width=True,
            height=force_display_all_rows(challenges_by_year),
            column_config={
                "QUERY_YEAR": st.column_config.TextColumn("Year"),
                "CUMULATIVE_USERS": st.column_config.TextColumn("Total Users"),
            },
        )
        st.bar_chart(
            challenges_by_year.sort_values("Year", ascending=False),
            x="Year",
            y="Number of Challenges",
            color="#38756a",
        )

    if selected_option == "Directory":
        # Add filter to sidebar
        year_filter = st.sidebar.multiselect(
            "Filter by Year(s)",
            challenges_by_year["Year"].sort_values(ascending=False).tolist(),
        )

        filtered_challenges = challenges[["Year", "NAME", "Link", "PROJECT_CREATOR"]]
        if len(year_filter):
            filtered_challenges = filtered_challenges.loc[
                filtered_challenges["Year"].isin(year_filter)
            ]
        st.dataframe(
            filtered_challenges,
            hide_index=True,
            use_container_width=True,
            height=force_display_all_rows(filtered_challenges),
            column_config={
                "NAME": st.column_config.TextColumn("Challenge Name"),
                "Link": st.column_config.LinkColumn(),
                "PROJECT_CREATOR": st.column_config.TextColumn(
                    "Synapse Point-of-Contact"
                ),
            },
        )

    if selected_option == "Data Downloads":
        st.markdown("Retrieve the number of challenge data downloads by challenge.")
        syn_id = st.text_input(
            "**Challenge Synapse ID**",
            max_chars=11,
            placeholder="syn12345678",
            help=(
                "The Challenge Synapse ID is the same as the Project SynID, "
                "which can be found in the top-left corner of the Project."
            ),
        )

        if syn_id:
            try:
                download_counts = get_data_from_snowflake(
                    query_data_download_counts(syn_id)
                )
                download_counts["NODE_ID"] = "syn" + download_counts["NODE_ID"].astype(str)
                st.dataframe(
                    download_counts,
                    hide_index=True,
                    use_container_width=True,
                    height=1000,
                    column_config={
                        "NODE_ID": st.column_config.TextColumn("Synapse ID", width="small"),
                        "FILENAME": st.column_config.TextColumn("Filename"),
                        "NUMBER_OF_DOWNLOADS": st.column_config.TextColumn(
                            "Download Count", width="small"
                        ),
                    },
                )
            except Exception:
                st.markdown(f":red[{syn_id} is not a valid ID, please try again.]")

    # 4. Basic footer
    # -------------------------------------------------------------------------
    st.markdown(footer_html(), unsafe_allow_html=True)


if __name__ == "__main__":
    app(SELECTED_OPTION)
