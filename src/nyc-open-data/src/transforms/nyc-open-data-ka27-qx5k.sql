-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cultural_institutions_group_cig",
    "fiscal_year_fy",
    "operating_support",
    "energy_support"
FROM "nyc-open-data-ka27-qx5k"
