-- Published pass-through of raw asset `cnam-medecins-optam-infra-annuelle`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "taux_adhesion_integer" AS optam_adhesion_rate_pct
FROM "cnam-medecins-optam-infra-annuelle"
