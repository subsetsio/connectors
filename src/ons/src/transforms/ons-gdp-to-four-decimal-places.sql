-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "mmm_yy",
    "time",
    "uk_only",
    "geography",
    "sic_unofficial",
    "unofficialstandardindustrialclassification"
FROM "ons-gdp-to-four-decimal-places"
