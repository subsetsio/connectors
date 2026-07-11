-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This indicator mixes monthly and annual periodicities; use id_periodicidade before comparing or aggregating periods.
SELECT
    "nom_fluxo",
    "id_periodicidade",
    "din_referencia",
    "val_atls",
    "num_horasviolacao"
FROM "ons-brazil-ind-confiarb-atls"
