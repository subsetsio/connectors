-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment",
    "industry_nace_rev_1_1",
    "value"
FROM "geostat-population-20census-202014-economic-20characteristics-16-1"
