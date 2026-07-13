-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are raw Movebank location or sensor events for one study and may mix individuals, tags, sensor types, and taxa; filter those dimensions before aggregating movement records.
SELECT
    CAST("event_id" AS BIGINT) AS event_id,
    "timestamp",
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("latitude" AS DOUBLE) AS latitude,
    "sensor_type",
    "taxon",
    CAST("individual_id" AS BIGINT) AS individual_id,
    CAST("tag_id" AS BIGINT) AS tag_id,
    "study_name"
FROM "movebank-move-1515"
