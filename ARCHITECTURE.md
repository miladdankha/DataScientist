# Shared dashboard architecture

| Stage | File and entry point | Responsibility |
|---|---|---|
| Download | `get_data.py` · `fetch` | Downloads both public 2026 files from Git LFS. Replaces each target only after verifying the temporary file’s SHA-256 checksum. |
| Load | `logic.py` · `load_survey` | Reads the 13 required columns, checks that every row has a unique `ResponseId`, and uses it as the index. |
| Analyze | `logic.py` · `population`, `ranking` | Selects respondents, splits multiple-choice answers, and calculates counts and percentages per question. These functions run independently of Streamlit. |
| Display | `app.py` · `cached_survey` and dashboard | Caches the loaded data, applies the selected filters, and displays the finding, chart, and full ranking. |

## Population and denominator

Respondents qualify if they selected “I create code as a primary part of my job” for `CodeMain`. The France view includes respondents whose reported `Country` of residence is France. The Outside France view requires a known country of residence other than France.

The five technology families use the survey column prefixes `Languages`, `Databases`, `WebFramework`, `DevIDE`, and `CloudPlat`. The last group includes containers and infrastructure tools. The suffix `HaveWorkedWith` describes use in the past year. `WantToWorkWith` describes what respondents want to use in the coming year. The exact wording for each question appears in `survey_results_schema.csv`.

For each family and measure, the denominator counts people who selected at least one option. The numerator counts distinct respondents who selected a particular technology. People could select multiple options, so the shares can add up to more than 100%. Selecting “Other, please specify” counts toward the denominator. Only named technologies appear in the ranking. Past and desired use can have different denominators. This version covers the 2026 survey.

## Cache, session state, and branches

`st.cache_data` retains the loaded columns between interactions. The cache key includes the file path and its modification time. Widgets store the current choices under the session keys `region`, `family`, and `metric`. The dashboard recalculates the ranking for the current selection.

The shared dashboard lives on `main`. Each team member can develop an analysis on a dedicated branch and reuse the common population and ranking functions. When adding a measure, define its denominator and unit in the analysis code before displaying it. The selector’s five technology families provide descriptive views. The team chooses the questions for its individual analyses.

## Language adoption

The entry point shares the cached survey and region filter between Overview and Language adoption using Streamlit navigation. Overview lives in `views/overview.py`. The adoption page in `views/language_adoption.py` adds a language selector and calls `logic.language_adoption_counts`. The function pairs each respondent’s past-use and desired-use answers, then splits those interested in each language into two mutually exclusive groups. Each percentage uses the number who answered both questions and want that language. Missing answers are excluded before classification.
