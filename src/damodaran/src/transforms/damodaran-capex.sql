-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `category` is the source's industry label and `region` includes aggregate market regions such as Global and Emerging; filter region before comparing industries across markets.
SELECT
    "region",
    "category",
    "metric",
    "value"
FROM "damodaran-capex"
