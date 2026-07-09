-- Published pass-through of raw asset `cnam-patients-longueduree-annuelle`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "taux_patients_ald_sans_mt_integer" AS ald_patients_without_attending_physician_pct
FROM "cnam-patients-longueduree-annuelle"
