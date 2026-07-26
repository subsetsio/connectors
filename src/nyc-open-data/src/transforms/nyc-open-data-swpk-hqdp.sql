-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "_year" AS year,
    "fips_county_code",
    "nta_code",
    "nta_name",
    "population"
FROM "nyc-open-data-swpk-hqdp"
