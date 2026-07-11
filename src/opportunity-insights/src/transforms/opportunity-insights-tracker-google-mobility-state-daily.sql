-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day",
    "statefips",
    "gps_retail_and_recreation",
    "gps_grocery_and_pharmacy",
    "gps_parks",
    "gps_transit_stations",
    "gps_workplaces",
    "gps_residential",
    "gps_away_from_home"
FROM "opportunity-insights-tracker-google-mobility-state-daily"
