-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are weekly aggregates split by confirmed-alert status; filter or explicitly aggregate the flag before comparing country-week totals.
SELECT
    "iso",
    "alert_week_start",
    "is_confirmed_alert",
    "alert_count",
    "alert_area_ha",
    "aboveground_co2_emissions_mg"
FROM "global-forest-watch-gadm--glad--iso-weekly-alerts"
