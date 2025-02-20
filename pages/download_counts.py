import streamlit as st

from toolkit.queries import query_challenge_info, query_data_download_counts
from toolkit.utils import force_display_all_rows, get_data_from_snowflake

st.subheader("Data Download Counts")
st.markdown("Get the download count for data files* for a given Challenge, using the latest snapshot.")
st.caption("*A challenge data file is assumed to be any file that is not `*.log` or `*predictions.csv`.")
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

challenge_name = ""
if syn_id:
    try:
        challenge_name = get_data_from_snowflake(query_challenge_info(syn_id)).loc[
            0, "NAME"
        ]
        download_counts = get_data_from_snowflake(query_data_download_counts(syn_id))
        download_counts["NODE_ID"] = "syn" + download_counts["NODE_ID"].astype(str)
        st.subheader(
            f"Challenge Name: [{challenge_name}](https://www.synapse.org/Synapse:{syn_id})"
        )
        st.caption(f"Files found: `{len(download_counts)}`")
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
    except KeyError:
        st.markdown(
            f":red[`{syn_id}` not found or may have been removed, "
            "please try a different synID.]"
        )
    except AttributeError:
        st.markdown(f":red[`{syn_id}` is not a valid synID, please try again.]")
