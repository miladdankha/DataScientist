import pandas as pd
import streamlit as st

from logic import language_adoption_counts


def render(group, region):
    st.title("Language adoption")
    st.write("Among professionals who want to use a language next year, how many already used it in the past year?")
    counts, paired = language_adoption_counts(group)
    if not counts:
        st.info("No respondents in this region named a desired language and answered both questions.")
        return
    languages = sorted(counts)
    default = languages.index("Rust") if "Rust" in counts else 0
    language = st.sidebar.selectbox("Language", languages, index=default, key="adoption_language")

    split = counts[language]
    total = sum(split.values())
    returning = split["Used last year"]
    prospective = total - returning
    st.header(f"{prospective:,} of {total:,} interested in {language} did not report using it last year")
    st.caption(f"2026 · {region} · Respondents who code as a primary part of their job · "
               f"{paired:,} answered both questions · {total:,} selected {language} for next year")
    table = pd.DataFrame(split.items(), columns=["Past-year experience", "Respondents"])
    table["Share (%)"] = 100 * table["Respondents"] / total
    st.vega_lite_chart(table, {
        "mark": {"type": "bar", "color": "#176B87"},
        "encoding": {
            "y": {"field": "Past-year experience", "type": "nominal", "sort": list(split), "title": None},
            "x": {"field": "Share (%)", "type": "quantitative", "scale": {"domain": [0, 100]},
                  "title": f"Share of respondents who want to use {language} (%)"},
            "tooltip": [{"field": "Past-year experience"}, {"field": "Respondents", "type": "quantitative"},
                        {"field": "Share (%)", "type": "quantitative", "format": ".1f"}],
        },
    }, width="stretch")
    st.dataframe(table, hide_index=True, column_config={"Share (%)": st.column_config.NumberColumn(format="%.1f%%")})
    st.subheader("What this suggests for teaching")
    st.write(f"For {language}, {prospective:,} interested respondents could inform the case for an "
             f"introductory lab. Another {returning:,} reported past-year use, a group whose needs "
             "could inform a follow-on project. Check students’ prior experience before choosing a course level.")
    with st.expander("How to read these numbers"):
        st.write("Each person counts once per language. Both survey items must contain an answer. "
                 "A person who selected a language for next year appears in exactly one of the two rows. "
                 "Someone who did not select it for last year may still have used it earlier. "
                 "The voluntary survey measures professional interests. It does not measure student demand.")
        st.markdown("[2026 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2026/)")
