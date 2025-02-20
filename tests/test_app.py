"""A suite of unit tests for the streamlit app in the base directory. We encourage
adding tests into this suite to ensure functionality within your streamlit app, particularly
for the components that allow users to interact with the app (buttons, dropdown menus, etc).

These tests were all written using Streamlit's AppTest class. See here for more details:
https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest#run-an-apptest-script

A few considerations:

1. This suite is meant to be run from the base directory, not from the tests directory.
2. The streamlit app is meant to be run from the base directory.
3. The streamlit app is assumed to be called ``app.py``.
"""

import os
import sys

import pytest
from streamlit.testing.v1 import AppTest

# Ensure that the base directory is in PYTHONPATH so ``toolkit`` and other tools can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# The timeout limit to wait for the app to load before shutdown ( in seconds )
DEFAULT_TIMEOUT = 30


@pytest.fixture(scope="module")
def app():
    return AppTest.from_file(
        "app.py", default_timeout=DEFAULT_TIMEOUT
    ).run()


# NOTE: Testing the app with navigation is currently not possible;
#       related GitHub issue here: https://github.com/streamlit/streamlit/issues/9446
# def test_app_with_navigation(app):
#     assert app.markdown[1].value == "### Dashboard"


# def test_switch_page_with_navigation(app):
#     assert app.markdown[1].value == "### Dashboard"

#     app.switch_page("pages/directory_list.py")
#     assert app.markdown[1].value == "### Directory of Challenges"

#     app.switch_page("pages/download_counts.py")
#     assert app.markdown[1].value == "### Data Download Counts"
