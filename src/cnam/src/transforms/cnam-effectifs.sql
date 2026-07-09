-- Published pass-through of raw asset `cnam-effectifs`.
-- `tri` (portal sort order) is dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "patho_niv1" AS pathology_level_1,
    "patho_niv2" AS pathology_level_2,
    "patho_niv3" AS pathology_level_3,
    "top" AS pathology_code,
    "cla_age_5" AS age_class_code,
    "libelle_classe_age" AS age_class,
    CAST("sexe" AS BIGINT) AS sex_code,
    "libelle_sexe" AS sex,
    "region" AS region_code,
    "dept" AS department_code,
    "ntop" AS patients,
    "npop" AS reference_population,
    "prev" AS prevalence_pct,
    "niveau_prioritaire" AS priority_levels
FROM "cnam-effectifs"
