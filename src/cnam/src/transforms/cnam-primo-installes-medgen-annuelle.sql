-- Published pass-through of raw asset `cnam-primo-installes-medgen-annuelle`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "effectif_primo_installe" AS first_time_installations,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-primo-installes-medgen-annuelle"
