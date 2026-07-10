-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date" AS BIGINT) AS date,
    "champ",
    "nombre_de_jint_y_compris_transports",
    "nombre_de_jint_hors_transports"
FROM "dares-dares-jint-1975-2004"
