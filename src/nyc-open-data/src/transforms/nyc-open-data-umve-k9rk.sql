-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "forecast_year",
    "forecasted_year_2",
    "scenario",
    "_source" AS source,
    "conversion_units",
    "conversion_value"
FROM "nyc-open-data-umve-k9rk"
