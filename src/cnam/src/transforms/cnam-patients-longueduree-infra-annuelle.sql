-- Published pass-through of raw asset `cnam-patients-longueduree-infra-annuelle`.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "taux_patients_ald_sans_mt" AS ald_patients_without_attending_physician_pct
FROM "cnam-patients-longueduree-infra-annuelle"
