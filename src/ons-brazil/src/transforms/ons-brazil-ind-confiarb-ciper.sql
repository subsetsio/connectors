-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This indicator mixes aggregation levels and periodicities; filter dsc_agregacao and id_periodicidade before aggregating.
SELECT
    "dsc_agregacao",
    "cod_caracteristica",
    "dsc_caracteristica",
    "id_periodicidade",
    "din_referencia",
    "val_ciper1",
    "val_ciper2",
    "val_ciper3",
    "val_ciper4",
    "val_ciper5"
FROM "ons-brazil-ind-confiarb-ciper"
