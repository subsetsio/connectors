-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are weekly aggregates split by alert confidence; filter or explicitly aggregate confidence categories before comparing country-week totals.
SELECT
    "iso",
    "alert_week_start",
    "confidence",
    "alert_count"
FROM "global-forest-watch-gadm--modis--iso-weekly-alerts"
