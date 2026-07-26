-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "accident_no",
    "date",
    "time",
    "borough",
    "street_name",
    "injuries_fatalities",
    "contributing_factors"
FROM "nyc-open-data-knr6-vurn"
