-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("din_instante" AS TIMESTAMP) AS din_instante,
    "val_carga_mw"
FROM "ons-brazil-cargaglobal-roraima"
