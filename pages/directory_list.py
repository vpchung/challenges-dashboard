
import streamlit as st

from toolkit.queries import query_challenges
from toolkit.utils import force_display_all_rows, get_data_from_snowflake

# DATA
# ------------------------------------------------------------------------
if "challenges" in st.session_state:
    challenges = st.session_state["challenges"]
else:
    challenges = get_data_from_snowflake(query_challenges())
    challenges["Year"] = challenges["DATE"].astype(str).str.split("-", expand=True)[0]

# Create new column for hyperlinks
challenges["Link"] = "https://www.synapse.org/Synapse:syn" + challenges[
    "PROJECT_ID"
].astype(str)


# APP
# ------------------------------------------------------------------------

st.markdown("### Directory of Challenges")

year_filter = st.multiselect(
    "Filter by Year(s)",
    challenges["Year"].sort_values(ascending=False).drop_duplicates().tolist(),
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
