-- Published pass-through of raw asset `cnam-medgen-zones-sous-dotees-annuelle`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "effectif_medecin_install_zsd" AS physicians_installed_in_underserved_zones,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-medgen-zones-sous-dotees-annuelle"
