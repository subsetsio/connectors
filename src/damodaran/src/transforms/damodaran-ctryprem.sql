-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `category` is a country or market label from the source, not a standardized country code.
SELECT
    "region",
    "category",
    "metric",
    "value"
FROM "damodaran-ctryprem"
