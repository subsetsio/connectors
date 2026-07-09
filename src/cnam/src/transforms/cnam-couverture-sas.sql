-- Published pass-through of raw asset `cnam-couverture-sas`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "couvert" AS covered,
    "taux_population_couverte_integer" AS population_covered_pct
FROM "cnam-couverture-sas"
