from pathlib import Path

import streamlit as st

from get_data import ANSWERS
from logic import FAMILIES, METRICS, load_survey, population, ranking

st.set_page_config(page_title="Technologies · École d’ingénieurs", layout="wide")


@st.cache_data(show_spinner="Lecture de l’enquête 2026…")
def cached_survey(path: Path, modification_ns: int):
    return load_survey(path)


st.title("Quelles technologies renforcer dans les enseignements ?")
st.caption("École d’ingénieurs · Stack Overflow Developer Survey 2026")
if not ANSWERS.is_file():
    st.info("Pour charger l’enquête officielle, exécutez la commande ci-dessous puis actualisez la page.")
    st.code("uv run python get_data.py", language="bash")
    st.stop()

survey = cached_survey(ANSWERS, ANSWERS.stat().st_mtime_ns)
with st.sidebar:
    st.header("Périmètre")
    region = st.radio("Lieu de résidence", ["France", "Hors France"], key="region")
    family = st.selectbox("Famille de technologies", list(FAMILIES), key="family")
    metric = st.radio("Indicateur", list(METRICS), key="metric")

group = population(survey, region)
table, n = ranking(group, family, metric)
scope = f"2026 · {region} · personnes dont le code est l’activité principale au travail"
st.caption(f"{scope} · {len(group):,} personnes dans le périmètre".replace(",", " "))
if table.empty:
    st.info(f"Aucune technologie nommée pour cette sélection ({n} réponses exploitables).")
    st.stop()

leaders = table.loc[table["Répondants"].eq(table.iloc[0]["Répondants"]), "Technologie"]
st.header(f"{', '.join(leaders)} en tête · {table.iloc[0]['Part (%)']:.1f} %")
if family == "Langages" and region == "France":
    findings = []
    for indicator, period in [("Usage déclaré", "l’année écoulée"), ("Usage souhaité", "l’année à venir")]:
        results, base = ranking(group, family, indicator)
        if not results.empty:
            count = results.iloc[0]["Répondants"]
            names = " et ".join(results.loc[results["Répondants"].eq(count), "Technologie"])
            findings.append(f"{names} en tête pour {period} ({count} sur {base})")
    st.write("Pour guider la révision des cours, le classement des langages place "
             + " et ".join(findings) + ".")
st.subheader(f"{family} · {metric.lower()}")
st.caption(f"{scope} · {n} répondants à cet item · dix premières technologies au maximum")
st.vega_lite_chart(table.head(10), {
    "mark": {"type": "bar", "color": "#176B87"},
    "encoding": {
        "x": {"field": "Part (%)", "type": "quantitative", "scale": {"domain": [0, 100]},
              "title": "Part des répondants (%)"},
        "y": {"field": "Technologie", "type": "nominal", "sort": "-x", "title": None},
        "tooltip": [{"field": "Technologie"}, {"field": "Répondants", "type": "quantitative"},
                    {"field": "Part (%)", "type": "quantitative", "format": ".1f"}],
    },
}, width="stretch")
with st.expander("Voir tous les effectifs et pourcentages"):
    st.dataframe(table, hide_index=True, column_config={"Part (%)": st.column_config.NumberColumn(format="%.1f %%")})
with st.expander("Source et méthode"):
    st.markdown("Source : [Stack Overflow Developer Survey 2026](https://survey.stackoverflow.co/2026/). "
                "Les participants sont volontaires. Le filtre géographique utilise le pays de résidence déclaré. "
                "Chaque part a pour base les répondants ayant donné au moins une réponse à l’item sélectionné. "
                "Les choix sont multiples. « Autre » compte dans la base et est exclu du classement. "
                "Les effectifs peuvent différer entre usages passés et souhaits futurs. "
                "Ces réponses éclairent les choix de cours sans mesurer la demande de recrutement.")
