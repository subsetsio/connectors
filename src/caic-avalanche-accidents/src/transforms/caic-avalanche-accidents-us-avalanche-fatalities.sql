-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Comprehensive national fatality workbook with historical coverage that is sparse before the modern CAIC era; some legacy rows have no stable source identifier and may repeat the same date, location, and description.
SELECT
    CAST("avy_year" AS INTEGER) AS avalanche_year,
    "date" AS accident_date,
    EXTRACT(year FROM "date")::INTEGER AS year,
    EXTRACT(month FROM "date")::INTEGER AS month,
    "location",
    "setting",
    "state",
    CASE WHEN "lat" = 0 AND "lon" = 0 THEN NULL ELSE "lat" END AS latitude,
    CASE WHEN "lat" = 0 AND "lon" = 0 THEN NULL ELSE "lon" END AS longitude,
    "primary_activity",
    "travel_mode",
    CAST("killed" AS INTEGER) AS killed,
    "description"
FROM "caic-avalanche-accidents-us-avalanche-fatalities"
WHERE "date" IS NOT NULL
