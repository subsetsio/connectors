-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table carries multiple reliability indicators and periodicities; filter cod_caracteristica and id_periodicidade before comparing values.
SELECT
    "dsc_agregacao",
    "cod_caracteristica",
    "dsc_caracteristica",
    "id_periodicidade",
    "din_referencia",
    "val_dreq",
    "val_freq"
FROM "ons-brazil-ind-confiarb-dreq-freq"
