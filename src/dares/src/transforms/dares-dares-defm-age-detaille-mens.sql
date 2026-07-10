-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("date", '%Y-%m')::DATE AS date,
    "champ",
    "type_de_donnees",
    "categorie",
    "age_detaille",
    "nombre_de_demandeurs_d_emploi"
FROM "dares-dares-defm-age-detaille-mens"
