-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Metrics are in long form and have different physical units; filter `metric` before aggregating `value`.
SELECT
    strptime("report_date", '%Y%m%d')::DATE AS report_date,
    "station",
    "metric",
    "value"
FROM "hong-kong-observatory-weather-radiation-report"
