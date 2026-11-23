"""Population and indicators shared by the dashboard and future analysis pages."""
import pandas as pd

PROFESSIONAL = "I create code as a primary part of my job"
FAMILIES = {
    "Langages": "Languages",
    "Bases de données": "Databases",
    "Frameworks web": "WebFramework",
    "Éditeurs et IDE": "DevIDE",
    "Cloud et infrastructure": "CloudPlat",
}
METRICS = {"Usage déclaré": "HaveWorkedWith", "Usage souhaité": "WantToWorkWith"}
COLUMNS = ["ResponseId", "Country", "CodeMain"] + [
    family + metric for family in FAMILIES.values() for metric in METRICS.values()
]


def load_survey(path):
    survey = pd.read_csv(path, usecols=COLUMNS, dtype="string")
    ids = survey["ResponseId"]
    if ids.hasnans or not ids.is_unique:
        raise ValueError("Identifiant répondant manquant ou dupliqué.")
    return survey.set_index("ResponseId")


def population(survey, region):
    country = survey["Country"]
    territories = {"France": country.eq("France"), "Hors France": country.notna() & country.ne("France")}
    return survey.loc[survey["CodeMain"].eq(PROFESSIONAL) & territories[region]]


def ranking(group, family, metric):
    """Each respondent counts once per option. 'Other' still counts in the base."""
    column = FAMILIES[family] + METRICS[metric]
    votes = group[column].dropna().str.split(";").explode().str.strip()
    votes = votes[votes.ne("")].rename("Technologie").reset_index().drop_duplicates()
    n = votes["ResponseId"].nunique()
    counts = votes.loc[votes["Technologie"].ne("Other, please specify"), "Technologie"].value_counts()
    table = counts.rename("Répondants").reset_index()
    table["Part (%)"] = 100 * table["Répondants"] / n if n else 0.0
    return table.sort_values(["Répondants", "Technologie"], ascending=[False, True], ignore_index=True), n
