-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city",
    "street_homeless_population",
    "general_population",
    "ratio_of_unsheltered_homeless_to_general_population"
FROM "nyc-open-data-8kiv-2ukd"
