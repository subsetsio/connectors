-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Station Code" AS station_code,
    "Station Name" AS station_name,
    CAST("Latitude" AS DOUBLE) AS latitude,
    CAST("Longitude" AS DOUBLE) AS longitude,
    "Elevation" AS elevation,
    "Coordinates" AS coordinates,
    "Active" AS active
FROM "instituto-de-estad-sticas-de-puerto-rico-1-weather-stations-active-and-inactive"
