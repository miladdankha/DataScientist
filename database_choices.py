import streamlit as st

from logic import FAMILIES, METRICS, ranking


def render(group, region):
    st.title("Database choices")
    st.write(
        "If students already learn PostgreSQL, which second database "
        "would make a useful comparison lab?"
    )

    family = "Databases"
    metric = "Past-year use"
    databases, answered = ranking(group, family, metric)

    if databases.empty:
        st.info("No named databases were reported by this group.")
        return

    names = sorted(databases["Technology"])
    starting_database = st.sidebar.selectbox(
        "Starting database",
        names,
        index=names.index("PostgreSQL") if "PostgreSQL" in names else 0,
        key="database_starting_database",
    )

    column = FAMILIES[family] + METRICS[metric]
    selections = group[column].dropna().str.split(";").explode().str.strip()
    user_ids = selections.index[selections.eq(starting_database)].unique()

    table, total = ranking(group.loc[user_ids], family, metric)
    table = table.loc[table["Technology"].ne(starting_database)].rename(
        columns={"Technology": "Database"}
    )

    st.subheader(f"What else did {starting_database} users report using?")
    st.caption(
        f"Stack Overflow Developer Survey 2026 · {region} · Respondents who "
        f"code as a primary part of their job · {total:,} used {starting_database} "
        f"out of {answered:,} who answered the database question."
    )

    if table.empty:
        st.info("This group reported no other named databases.")
        return

    st.vega_lite_chart(
        table.head(10),
        {
            "mark": {"type": "bar", "color": "#176B87"},
            "encoding": {
                "x": {
                    "field": "Share (%)",
                    "type": "quantitative",
                    "scale": {"domain": [0, 100]},
                    "title": f"Share of {starting_database} users (%)",
                },
                "y": {
                    "field": "Database",
                    "type": "nominal",
                    "sort": "-x",
                    "title": None,
                },
                "tooltip": [
                    {"field": "Database"},
                    {"field": "Respondents", "type": "quantitative"},
                    {"field": "Share (%)", "type": "quantitative", "format": ".1f"},
                ],
            },
        },
        width="stretch",
    )

    with st.expander("View all counts and percentages"):
        st.dataframe(
            table,
            hide_index=True,
            column_config={
                "Share (%)": st.column_config.NumberColumn(format="%.1f%%"),
            },
        )

    counts = table.set_index("Database")["Respondents"]
    if starting_database == "PostgreSQL" and {"SQLite", "Redis"} <= set(counts.index):
        st.subheader("Two options for the lab")
        st.write(
            f"Of the {total:,} PostgreSQL users, {counts['SQLite']:,} also "
            f"reported SQLite and {counts['Redis']:,} reported Redis. "
            "SQLite suits a lab comparing server-based and embedded relational "
            "databases. Redis suits a lab on adding caching to an application."
        )

    st.caption(
        f"Percentages are based on the {total:,} respondents who selected "
        f"{starting_database}. Respondents could select multiple databases. "
        "Two selections indicate use by the same respondent during the past year. "
        "Whether that use occurred on the same project is unknown."
    )