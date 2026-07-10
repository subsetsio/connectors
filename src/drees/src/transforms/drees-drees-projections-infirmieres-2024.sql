-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "scenario",
    "mode_d_exercice",
    "tranche_d_age",
    "sexe",
    "nombre_d_infirmieres_en_emploi"
FROM "drees-drees-projections-infirmieres-2024"
