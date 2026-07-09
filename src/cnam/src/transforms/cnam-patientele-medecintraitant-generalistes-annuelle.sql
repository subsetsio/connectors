-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `nombre_patients_medecin_traitant` is a mean panel size per general practitioner, not a total. The territory columns mix département, région and national rows.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_patients_medecin_traitant",
    "taux_evolution_annuel",
    "taux_evolution_annuel_integer"
FROM "cnam-patientele-medecintraitant-generalistes-annuelle"
