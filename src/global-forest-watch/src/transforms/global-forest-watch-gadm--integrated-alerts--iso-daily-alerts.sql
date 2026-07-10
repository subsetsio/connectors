-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are monthly aggregates of a daily alert product; confidence is part of the grain, so filter or explicitly aggregate confidence categories before comparing totals.
SELECT
    "iso",
    "alert_month",
    "confidence",
    "alert_count",
    "alert_area_ha",
    "aboveground_co2_emissions_mg"
FROM "global-forest-watch-gadm--integrated-alerts--iso-daily-alerts"
