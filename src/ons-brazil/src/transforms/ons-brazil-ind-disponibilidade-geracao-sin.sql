-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("dat_referencia", '%Y-%m-%d')::DATE AS dat_referencia,
    "val_dispf",
    "val_indisppf",
    "val_indispff"
FROM "ons-brazil-ind-disponibilidade-geracao-sin"
