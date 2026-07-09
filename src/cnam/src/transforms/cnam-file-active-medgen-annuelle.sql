-- Published pass-through of raw asset `cnam-file-active-medgen-annuelle`.
-- French-formatted measure strings are dropped for their parsed numeric twins.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "nombre_patients_uniques_integer" AS mean_unique_patients,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-file-active-medgen-annuelle"
