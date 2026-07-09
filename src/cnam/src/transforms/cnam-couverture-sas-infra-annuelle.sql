-- Published pass-through of raw asset `cnam-couverture-sas-infra-annuelle`.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "couvert" AS covered,
    "taux_population_couverte" AS population_covered_pct
FROM "cnam-couverture-sas-infra-annuelle"
