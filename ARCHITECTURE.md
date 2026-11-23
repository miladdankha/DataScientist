# Architecture du socle commun

Le parcours d’un chiffre suit quatre étapes.

| Étape | Fichier et point d’entrée | Responsabilité |
|---|---|---|
| Acquisition | `get_data.py · fetch` | Récupère les deux objets Git LFS publics 2026. Un fichier temporaire remplace sa cible après vérification SHA-256. |
| Chargement | `logic.py · load_survey` | Lit les 13 colonnes utiles, vérifie l’unicité et la présence de ResponseId, puis utilise cet identifiant comme index. |
| Population et calcul | `logic.py · population, ranking` | Sélectionne la population, décompose les réponses multiples et calcule les effectifs et pourcentages par item. Ces fonctions sont indépendantes de Streamlit. |
| Interface | `app.py · cached_survey` et dashboard | Met en cache la lecture du CSV, applique les sélections, puis présente le constat, le classement et le tableau détaillé. |

## Population et dénominateur

Le critère professionnel est la réponse « I create code as a primary part of my job » à CodeMain. Country contient le pays de résidence. La vue France retient France et la vue hors France exige un pays connu différent de France.

Les cinq familles correspondent aux préfixes Languages, Databases, WebFramework, DevIDE et CloudPlat. Cette dernière famille inclut aussi les conteneurs et les outils d’infrastructure. Le suffixe HaveWorkedWith renseigne la pratique au cours de l’année écoulée et WantToWorkWith les souhaits pour l’année à venir. Les formulations détaillées de chaque item figurent dans survey_results_schema.csv.

Pour une famille et un indicateur, le dénominateur est le nombre de personnes ayant coché au moins une option. Le numérateur est le nombre de répondants distincts ayant coché la technologie. Les choix multiples peuvent porter la somme des parts au-delà de 100 %. Une réponse « Other, please specify » compte dans le dénominateur. Les bases de l’usage et du souhait peuvent différer. La première édition du socle porte uniquement sur 2026.

## Cache, session et branches

`st.cache_data` conserve les colonnes chargées entre les interactions. La clé inclut le chemin et la date de modification du fichier. Les widgets portent les clés de session `region`, `family` et `metric`. Le classement est recalculé sur la sélection courante.

Le dashboard commun vit sur main. Chaque membre peut développer son axe sur une branche dédiée en réutilisant la population et les calculs communs. Pour ajouter un indicateur, définir sa base et son unité dans la logique avant de l’afficher dans une vue. Les cinq familles du sélecteur sont des vues descriptives du socle ; les axes individuels seront définis par le groupe.
