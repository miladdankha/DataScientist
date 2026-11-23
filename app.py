from pathlib import Path

import streamlit as st

from get_data import ANSWERS, SCHEMA, fetch
from logic import load_survey, population
from views import language_adoption, overview

st.set_page_config(page_title="Technologies · Engineering School", layout="wide")


@st.cache_data(show_spinner="Loading the 2026 survey…")
def cached_survey(path: Path, modification_ns: int):
    return load_survey(path)


if not ANSWERS.is_file() or not SCHEMA.is_file():
    try:
        with st.spinner("Downloading and verifying the official survey files…"):
            fetch()
    except (OSError, ValueError) as exc:
        st.error(f"The survey files could not be loaded: {exc}")
        if st.button("Retry download"):
            st.rerun()
        st.stop()

survey = cached_survey(ANSWERS, ANSWERS.stat().st_mtime_ns)
with st.sidebar:
    st.header("Survey filters")
    region = st.radio("Country of residence", ["France", "Outside France"], key="region")

group = population(survey, region)


def overview_page():
    overview.render(group, region)


def adoption_page():
    language_adoption.render(group, region)


st.navigation([
    st.Page(overview_page, title="Overview", default=True),
    st.Page(adoption_page, title="Language adoption", url_path="language-adoption"),
]).run()
