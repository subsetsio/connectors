-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This indicator mixes aggregation levels and periodicities; filter cod_tipoagregacao and id_periodicidade before aggregating.
SELECT
    "cod_tipoagregacao",
    "id_periodicidade",
    "nom_agregacao",
    "din_referencia",
    "num_linhasoperacao",
    "num_linhasvioladas",
    "val_ccal"
FROM "ons-brazil-ind-confiarb-ccal"
