-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `nombre_patients_uniques` and `nombre_patients_medecin_traitant` are means per practitioner (also shipped as parsed `*_integer` columns), not territory totals.
-- caution: The territory columns mix département, région and national rows.
SELECT
    "annee",
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_patients_uniques",
    "nombre_patients_medecin_traitant",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire",
    "patients_medecin_traitant_integer",
    "patients_uniques_integer"
FROM "cnam-patientele"
