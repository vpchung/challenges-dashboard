import streamlit as st
from snowflake.snowpark import Session


@st.cache_resource
def connect_to_snowflake():
    session = Session.builder.configs(st.secrets.snowflake).create()
    return session


@st.cache_data
def get_data_from_snowflake(query=""):
    session = connect_to_snowflake()
    node_latest = session.sql(query).to_pandas()
    return node_latest


def human_format(num: int) -> str:
    """Convert number to more human-readable format."""
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format("{:f}".format(num).rstrip(r"\.0"), ["", "k", "m", "b"][magnitude])


def force_display_all_rows(df) -> int:
    return 35 * len(df) + 38
