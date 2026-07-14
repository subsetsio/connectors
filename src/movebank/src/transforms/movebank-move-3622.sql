-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are raw Movebank location or sensor events for one study and may mix individuals, tags, sensor types, and taxa; filter those dimensions before aggregating movement records.
-- caution: `timestamp` is not a TIMESTAMP: the upstream export writes the seconds
-- field as `0S` on every row (`2019-02-24 01:31:0S`), so it is published verbatim.
SELECT
    CAST("event_id" AS BIGINT) AS event_id,
    "timestamp",
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("latitude" AS DOUBLE) AS latitude,
    "sensor_type",
    "taxon",
    "individual_id",
    "tag_id",
    "study_name"
FROM "movebank-move-3622"
