-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "forecast_year",
    "scenario",
    "sector",
    "_source" AS source,
    "activity_unit",
    "activity_value",
    "metric_tons_of_co2e",
    "tons_of_pm25"
FROM "nyc-open-data-czei-7bxd"
