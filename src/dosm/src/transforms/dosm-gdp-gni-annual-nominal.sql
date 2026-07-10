-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "series",
    "date",
    "gdp",
    "gni",
    "gdp_capita",
    "gni_capita"
FROM "dosm-gdp-gni-annual-nominal"
