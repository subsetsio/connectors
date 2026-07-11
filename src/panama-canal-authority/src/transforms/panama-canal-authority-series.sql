-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Use this table as the series catalog; it describes monitoring series and their locations, not observations.
SELECT
    "series_id",
    "parameter",
    "label",
    "location_identifier",
    "location_name",
    "location_type",
    "watershed",
    "latitude",
    "longitude",
    CAST("start_time" AS TIMESTAMP) AS start_time,
    CAST("end_time" AS TIMESTAMP) AS end_time,
    "timezone"
FROM "panama-canal-authority-series"
