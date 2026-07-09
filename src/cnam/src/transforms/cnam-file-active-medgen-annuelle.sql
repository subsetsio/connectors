-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `nombre_patients_uniques` is a mean patient panel per practitioner, not a total — it cannot be summed across territories or professions.
-- caution: The territory columns mix département, région and national rows.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "profession_sante",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_patients_uniques",
    "taux_evolution_annuel",
    "nombre_patients_uniques_integer",
    "taux_evolution_annuel_integer"
FROM "cnam-file-active-medgen-annuelle"
