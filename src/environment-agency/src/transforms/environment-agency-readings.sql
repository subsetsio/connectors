-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The value column mixes units and observed properties across measures; join to measures before comparing, aggregating, or labeling values.
SELECT
    "measure_id",
    "station_guid",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    CAST("date_time" AS TIMESTAMP) AS date_time,
    "value",
    "completeness",
    "quality"
FROM "environment-agency-readings"
