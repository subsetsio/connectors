-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table mixes monthly and annual frequency-performance observations; use id_periodicidade before comparing periods.
SELECT
    "id_periodicidade",
    "din_referencia",
    "id_faixafrequencia",
    "nom_faixafrequencia",
    "val_dfd"
FROM "ons-brazil-ind-qualid-dfd-meano"
