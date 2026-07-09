-- Published pass-through of raw asset `cnam-demographie-secteurs-conventionnels`.
-- the `vision_*` portal display flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "secteur_conventionnel" AS sector_code,
    "libelle_secteur_conventionnel" AS sector,
    "effectif" AS headcount
FROM "cnam-demographie-secteurs-conventionnels"
