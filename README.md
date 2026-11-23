# Observatoire des technologies · Stack Overflow 2026

Application Streamlit pour une école d’ingénieurs française. Elle éclaire la question « Quels langages et outils l’école devrait-elle renforcer dans ses enseignements l’an prochain ? »

## Lancement depuis un clone neuf

Prérequis : Git, [uv](https://docs.astral.sh/uv/) et un accès réseau au premier lancement. Depuis le terminal :

```sh
git clone https://github.com/miladdankha/DataScientist.git
cd DataScientist
uv sync --locked
uv run python get_data.py
uv run streamlit run app.py
```

Ouvrir l’adresse locale indiquée par Streamlit. Python 3.12 est déclaré dans le projet. Le téléchargement récupère les réponses publiques et le dictionnaire 2026 dans `data/` et vérifie leur empreinte SHA-256. Ces deux CSV restent locaux. Les lancements suivants peuvent réutiliser les fichiers.

## Lire le dashboard

La vue initiale présente les langages utilisés par les répondants professionnels vivant en France. Le panneau latéral permet de choisir le territoire, la famille de technologies et l’indicateur. Chaque graphique affiche la base de calcul. Le tableau dépliable donne les résultats complets.

Les réponses proviennent d’une enquête volontaire. Le lieu de résidence ne renseigne ni le pays de l’employeur ni le marché de recrutement. La comparaison hors France est descriptive et ne corrige pas les différences de composition des groupes.

[Architecture et conventions des futurs axes](ARCHITECTURE.md) · [Questionnaire, données et licence](https://github.com/StackExchange/Survey/tree/main/packages/archive/2026)
