-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "administrative_geography",
    "geography",
    "sic_unofficial",
    "unofficialstandardindustrialclassification",
    "type_of_prices",
    "prices"
FROM "ons-gva-by-industry-by-local-authority"
