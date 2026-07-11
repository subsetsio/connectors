-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table mixes daily, monthly, and annual permanent-regime frequency observations; filter the periodicity column before comparing periods.
SELECT
    "id_periodicidade",
    "din_referencia",
    "num_desvio_perm_sobre",
    "num_desvio_perm_sub",
    "num_desvio_dist_sobre",
    "num_desvio_dist_sub",
    "num_minutos",
    "val_dfp"
FROM "ons-brazil-ind-qualid-dfp-regime"
