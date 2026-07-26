-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "forecast_year",
    "forecast_description",
    "health_event",
    "number_of_avoided_health_events"
FROM "nyc-open-data-v988-8fd7"
