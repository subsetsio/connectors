-- Published pass-through of raw asset `cnam-patientele`.
-- French-formatted measure strings are dropped for their parsed numeric twins; the `vision_*` portal flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "patients_uniques_integer" AS mean_unique_patients,
    "patients_medecin_traitant_integer" AS mean_attending_physician_patients
FROM "cnam-patientele"
