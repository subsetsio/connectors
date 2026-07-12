-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source repeats some industry, tax-rate metric, and region labels for distinct tax-rate variants; filter to the intended metric rows before comparing or aggregating.
SELECT
    "region",
    "category",
    "metric",
    "value"
FROM "damodaran-taxrate"
