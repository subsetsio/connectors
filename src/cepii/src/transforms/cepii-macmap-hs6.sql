-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Applied tariff observations are importer-exporter-product specific; tariff lines are not additive trade values.
SELECT
    "reporter",
    "partner",
    "hs2",
    "adv",
    "w_rg"
FROM "cepii-macmap-hs6"
