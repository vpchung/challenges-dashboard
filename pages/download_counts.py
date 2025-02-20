import streamlit as st

from toolkit.queries import query_data_download_counts
from toolkit.utils import force_display_all_rows, get_data_from_snowflake

st.markdown("### Data Download Counts")
st.markdown("Find out how many times data files have been downloaded in a challenge.")
st.caption(":orange[⚠️ Query will not return `*.log` or `predictions.csv` files.]")
syn_id = st.text_input(
    "**Challenge Synapse ID**",
    max_chars=11,
    placeholder="syn12345678",
    help=(
        "A Challenge Synapse ID is the same as the Project SynID, "
        "which can be found in the top-left corner of a Synapse Project."
    ),
)
st.divider()

if syn_id:
    try:
        download_counts = get_data_from_snowflake(
            query_data_download_counts(syn_id)
        )
        download_counts["NODE_ID"] = "syn" + download_counts["NODE_ID"].astype(str)
        st.caption(f"Files found in the challenge: `{len(download_counts)}`")
        st.dataframe(
            download_counts,
            hide_index=True,
            use_container_width=True,
            height=force_display_all_rows(download_counts),
            column_config={
                "NODE_ID": st.column_config.TextColumn("Synapse ID", width=5),
                "FILENAME": st.column_config.TextColumn("Filename", width="large"),
                "NUMBER_OF_DOWNLOADS": st.column_config.TextColumn(
                    "Download Count", width=5
                ),
            },
        )
    except AttributeError:
        st.markdown(f":red[{syn_id} is not a valid ID, please try again.]")
