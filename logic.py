"""Population and indicators shared by the dashboard and future analysis pages."""
import pandas as pd

PROFESSIONAL = "I create code as a primary part of my job"
FAMILIES = {
    "Languages": "Languages",
    "Databases": "Databases",
    "Web frameworks": "WebFramework",
    "Editors and IDEs": "DevIDE",
    "Cloud and infrastructure": "CloudPlat",
}
METRICS = {"Past-year use": "HaveWorkedWith", "Desired use next year": "WantToWorkWith"}
COLUMNS = ["ResponseId", "Country", "CodeMain"] + [
    family + metric for family in FAMILIES.values() for metric in METRICS.values()
]


def load_survey(path):
    survey = pd.read_csv(path, usecols=COLUMNS, dtype="string")
    ids = survey["ResponseId"]
    if ids.hasnans or not ids.is_unique:
        raise ValueError("Missing or duplicate respondent ID.")
    return survey.set_index("ResponseId")


def population(survey, region):
    country = survey["Country"]
    territories = {"France": country.eq("France"), "Outside France": country.notna() & country.ne("France")}
    return survey.loc[survey["CodeMain"].eq(PROFESSIONAL) & territories[region]]


def ranking(group, family, metric):
    """Each respondent counts once per option. 'Other' still counts in the base."""
    column = FAMILIES[family] + METRICS[metric]
    votes = group[column].dropna().str.split(";").explode().str.strip()
    votes = votes[votes.ne("")].rename("Technology").reset_index().drop_duplicates()
    n = votes["ResponseId"].nunique()
    counts = votes.loc[votes["Technology"].ne("Other, please specify"), "Technology"].value_counts()
    table = counts.rename("Respondents").reset_index()
    table["Share (%)"] = 100 * table["Respondents"] / n if n else 0.0
    return table.sort_values(["Respondents", "Technology"], ascending=[False, True], ignore_index=True), n
