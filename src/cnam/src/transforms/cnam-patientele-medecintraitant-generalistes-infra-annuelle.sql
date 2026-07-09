-- Published pass-through of raw asset `cnam-patientele-medecintraitant-generalistes-infra-annuelle`.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "nombre_patients_medecin_traitant" AS mean_attending_physician_patients,
    "taux_evolution_annuel" AS annual_change_pct
FROM "cnam-patientele-medecintraitant-generalistes-infra-annuelle"
