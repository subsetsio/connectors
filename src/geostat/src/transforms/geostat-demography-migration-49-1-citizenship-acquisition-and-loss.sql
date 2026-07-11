-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acquisition_loss",
    "year",
    "value"
FROM "geostat-demography-migration-49-1-citizenship-acquisition-and-loss"
