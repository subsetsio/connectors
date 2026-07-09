-- Published pass-through of raw asset `cnam-demographie-effectifs-et-les-densites`.
-- the `vision_*` portal display flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "classe_age" AS age_class_code,
    "libelle_classe_age" AS age_class,
    "libelle_sexe" AS sex,
    "effectif" AS headcount,
    "densite" AS density
FROM "cnam-demographie-effectifs-et-les-densites"
