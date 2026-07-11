-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source notes that this precipitation series is no longer updated; treat freshness as frozen historical coverage.
SELECT
    "cod_estacao",
    "val_latitude",
    "val_longitude",
    "val_medida",
    "dat_observada"
FROM "ons-brazil-precipitacao-estacao"
