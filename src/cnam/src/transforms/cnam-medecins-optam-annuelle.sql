-- Published pass-through of raw asset `cnam-medecins-optam-annuelle`.
-- French-formatted measure strings are dropped for their parsed numeric twins.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "effectif_medecin_optam" AS optam_physicians,
    "taux_adhesion_integer" AS optam_adhesion_rate_pct,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-medecins-optam-annuelle"
