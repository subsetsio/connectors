-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "incident_key",
    "perp_id",
    "perp_age_group",
    "perp_sex",
    "perp_race"
FROM "nyc-open-data-gdk4-mbsv"
