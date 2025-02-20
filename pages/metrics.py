import streamlit as st

from toolkit.queries import query_challenges
from toolkit.utils import force_display_all_rows, get_data_from_snowflake, human_format

# DATA
# ------------------------------------------------------------------------
challenges = get_data_from_snowflake(query_challenges())
challenges["Year"] = challenges["DATE"].astype(str).str.split("-", expand=True)[0]
st.session_state["challenges"] = challenges

challenges_by_year = (
    challenges.groupby("Year").size().reset_index(name="Number of Challenges")
)

# Get general metrics and delta numbers for:
#   - challenges
#   - participants
#   - submissions
num_challenges = len(challenges)
delta_challenges = challenges_by_year["Number of Challenges"].diff().iloc[-1]
delta_participants = 8_100
delta_submissions = 65_420


# APP
# ------------------------------------------------------------------------

# Section: general metrics
st.markdown("### Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Challenges", num_challenges, int(delta_challenges))
col2.metric("Participants", human_format(delta_participants), "5%")
col3.metric("Submissions", human_format(delta_submissions))

st.divider()

# Section: Plot + table of challenges by year
st.markdown("##### Challenges By Year")
chart, table = st.columns([3, 1])
chart.bar_chart(
    challenges_by_year.sort_values("Year", ascending=False),
    x="Year",
    y="Number of Challenges",
    height=force_display_all_rows(challenges_by_year),
    color="#38756a",
)
table.dataframe(
    challenges_by_year.sort_values("Year", ascending=False),
    hide_index=True,
    height=force_display_all_rows(challenges_by_year),
    column_config={
        "QUERY_YEAR": st.column_config.TextColumn("Year"),
        "CUMULATIVE_USERS": st.column_config.TextColumn("Total Users"),
    },
)
