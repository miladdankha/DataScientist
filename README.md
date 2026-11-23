# Technology Observatory · Stack Overflow 2026

Which languages and tools should a French engineering school emphasize in next year’s curriculum? This Streamlit dashboard explores what professionals used in the past year and what they want to use next year.

## Run from a fresh clone

Install Git and [uv](https://docs.astral.sh/uv/). The first run requires an internet connection.

```sh
git clone https://github.com/miladdankha/DataScientist.git
cd DataScientist
uv sync --locked
uv run python get_data.py
uv run streamlit run app.py
```

Open the local URL printed by Streamlit. The project uses Python 3.12. The download script saves the public responses and survey schema in `data/` and verifies each file’s SHA-256 checksum. Both CSVs stay local and can be reused on subsequent runs.

## Read the dashboard

The dashboard opens with languages used by respondents living in France who code as a primary part of their job. Use the sidebar to change the region, technology family, or measure. Each chart shows how many people answered that question. Expand the table to see the full ranking.

Participation was voluntary. The geographic filter describes where respondents live. It provides no direct measure of employer location or hiring demand. Comparisons with respondents outside France are descriptive and do not adjust for differences in group composition.

[Architecture and guidance for analysis pages](ARCHITECTURE.md) · [Survey files, questionnaire, and license](https://github.com/StackExchange/Survey/tree/main/packages/archive/2026)
