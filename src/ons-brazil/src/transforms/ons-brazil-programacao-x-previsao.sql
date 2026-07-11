-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table compares forecast and scheduled values for wind and solar plants; keep forecast and scheduled measures distinct in aggregations.
SELECT
    CAST("dat_programacao" AS BIGINT) AS dat_programacao,
    "num_patamar",
    "cod_usinapdp",
    "nom_usinapdp",
    CAST("val_previsao" AS DOUBLE) AS val_previsao,
    CAST("val_programado" AS DOUBLE) AS val_programado
FROM "ons-brazil-programacao-x-previsao"
