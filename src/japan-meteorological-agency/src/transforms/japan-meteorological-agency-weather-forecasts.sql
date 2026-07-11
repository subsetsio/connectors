-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an operational forecast product: rows are forward-looking values issued at `report_datetime`, and later runs replace the active forecast horizon rather than extending a permanent history.
SELECT
    "office_code",
    "publishing_office",
    CAST("report_datetime" AS TIMESTAMP) AS report_datetime,
    "area_code",
    "area_name",
    "element",
    CAST("valid_time" AS TIMESTAMP) AS valid_time,
    "value"
FROM "japan-meteorological-agency-weather-forecasts"
