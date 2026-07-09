-- Published pass-through of raw asset `cnam-patientele-medecintraitant-generalistes-annuelle`.
-- the French-formatted rate string is dropped for its parsed numeric twin.
SELECT
    CAST("annee" AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "nombre_patients_medecin_traitant" AS mean_attending_physician_patients,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-patientele-medecintraitant-generalistes-annuelle"
