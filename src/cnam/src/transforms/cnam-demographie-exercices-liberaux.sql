-- Published pass-through of raw asset `cnam-demographie-exercices-liberaux`.
-- the `vision_*` portal display flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "type_exercice_liberal" AS practice_type_code,
    "libelle_type_exercice_liberal" AS practice_type,
    "effectif" AS headcount
FROM "cnam-demographie-exercices-liberaux"
