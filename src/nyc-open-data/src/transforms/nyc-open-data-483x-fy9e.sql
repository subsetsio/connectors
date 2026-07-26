-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city",
    "street_homeless_estimate",
    "general_population",
    "ratio"
FROM "nyc-open-data-483x-fy9e"
