-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table combines many Journey North map layers and event types; filter or group by `map_slug` before interpreting counts as a specific species, life stage, or seasonal event.
SELECT
    CAST("sighting_id" AS BIGINT) AS sighting_id,
    "map_slug",
    "year",
    "season",
    strptime("date", '%m/%d/%Y')::DATE AS date,
    "observed_unix",
    "longitude",
    "latitude",
    "elevation",
    "interval",
    "pin_id",
    "duration",
    "image_url"
FROM "journey-north-sightings"
