-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id_postofluv" AS BIGINT) AS id_postofluv,
    "nom_postofluviometrico",
    "val_latitude",
    "val_longitude",
    "nom_rio",
    "nom_bacia",
    strptime("din_medicao", '%Y-%m-%d')::DATE AS din_medicao,
    "val_vazaomedia",
    "val_vazaomediaincr"
FROM "ons-brazil-grandezas-fluviometricas"
