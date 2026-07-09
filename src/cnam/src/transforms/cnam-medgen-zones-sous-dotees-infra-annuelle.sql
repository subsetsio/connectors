-- Published pass-through of raw asset `cnam-medgen-zones-sous-dotees-infra-annuelle`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "effectif_medecin_install_zsd" AS physicians_installed_in_underserved_zones,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-medgen-zones-sous-dotees-infra-annuelle"
