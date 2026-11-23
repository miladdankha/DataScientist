from pathlib import Path

import streamlit as st

from get_data import ANSWERS
from logic import FAMILIES, METRICS, load_survey, population, ranking

st.set_page_config(page_title="Technologies · Engineering School", layout="wide")


@st.cache_data(show_spinner="Loading the 2026 survey…")
def cached_survey(path: Path, modification_ns: int):
    return load_survey(path)


st.title("Which languages and tools should the school emphasize next year?")
st.caption("Engineering curriculum · 2026 Stack Overflow Developer Survey")
if not ANSWERS.is_file():
    st.info("Run the command below to download the official survey, then refresh this page.")
    st.code("uv run python get_data.py", language="bash")
    st.stop()

survey = cached_survey(ANSWERS, ANSWERS.stat().st_mtime_ns)
with st.sidebar:
    st.header("Survey filters")
    region = st.radio("Country of residence", ["France", "Outside France"], key="region")
    family = st.selectbox("Technology family", list(FAMILIES), key="family")
    metric = st.radio("Measure", list(METRICS), key="metric")

group = population(survey, region)
table, n = ranking(group, family, metric)
scope = f"2026 · {region} · respondents who code as a primary part of their job"
st.caption(f"{scope} · {len(group):,} respondents in this group")
if table.empty:
    st.info(f"No named technologies for this selection ({n:,} respondents answered the question).")
    st.stop()

leaders = table.loc[table["Respondents"].eq(table.iloc[0]["Respondents"]), "Technology"]
st.header(f"{', '.join(leaders)} · {table.iloc[0]['Share (%)']:.1f}% of respondents")
if family == "Languages" and region == "France":
    findings = []
    for indicator, period in [("Past-year use", "Most used in the past year"), ("Desired use next year", "Most wanted for next year")]:
        results, base = ranking(group, family, indicator)
        if not results.empty:
            count = results.iloc[0]["Respondents"]
            names = " and ".join(results.loc[results["Respondents"].eq(count), "Technology"])
            findings.append(f"{period}: {names} ({count:,} of {base:,} respondents)")
    st.write(" · ".join(findings))
st.subheader(f"{family} · {metric.lower()}")
st.caption(f"{scope} · {n:,} respondents answered this question · up to 10 leading technologies")
st.vega_lite_chart(table.head(10), {
    "mark": {"type": "bar", "color": "#176B87"},
    "encoding": {
        "x": {"field": "Share (%)", "type": "quantitative", "scale": {"domain": [0, 100]},
              "title": "Share of respondents (%)"},
        "y": {"field": "Technology", "type": "nominal", "sort": "-x", "title": None},
        "tooltip": [{"field": "Technology"}, {"field": "Respondents", "type": "quantitative"},
                    {"field": "Share (%)", "type": "quantitative", "format": ".1f"}],
    },
}, width="stretch")
with st.expander("View all counts and percentages"):
    st.dataframe(table, hide_index=True, column_config={"Share (%)": st.column_config.NumberColumn(format="%.1f%%")})
with st.expander("Source and methodology"):
    st.markdown(
        "The survey is voluntary. Geography reflects each respondent’s reported country of residence. "
        "Each percentage uses the number of people who selected at least one option for that question. "
        "Respondents could select several technologies. The denominator includes people who chose "
        "‘Other, please specify’. The ranking shows named technologies only. "
        "Past use and desired use can have different response counts. These answers can guide "
        "curriculum decisions. Hiring demand would require separate evidence. "
        "[2026 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2026/)"
    )
