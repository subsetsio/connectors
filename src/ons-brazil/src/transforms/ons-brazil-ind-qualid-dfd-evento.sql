-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "din_referencia",
    "din_iniciodesviofreq",
    "din_fimdesviofreq",
    "id_faixafrequencia",
    "nom_faixafrequencia",
    "val_dfd",
    "val_freqmaxmin"
FROM "ons-brazil-ind-qualid-dfd-evento"
