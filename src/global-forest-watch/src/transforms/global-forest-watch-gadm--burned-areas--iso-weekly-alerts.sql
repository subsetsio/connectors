-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "iso",
    "alert_week_start",
    "burned_area_ha"
FROM "global-forest-watch-gadm--burned-areas--iso-weekly-alerts"
