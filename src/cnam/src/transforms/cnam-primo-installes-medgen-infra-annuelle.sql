-- Published pass-through of raw asset `cnam-primo-installes-medgen-infra-annuelle`.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "effectif_primo_installe" AS first_time_installations,
    "taux_evolution_annuel" AS annual_change_pct
FROM "cnam-primo-installes-medgen-infra-annuelle"
