-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "nuts",
    "geography",
    "sic_unofficial",
    "unofficialstandardindustrialclassification",
    "type_of_prices",
    "prices",
    "quarterly_index_and_growth_rate",
    "growthrate"
FROM "ons-regional-gdp-by-year"
