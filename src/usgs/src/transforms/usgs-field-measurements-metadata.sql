-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A field measurement series identifier can appear in multiple metadata versions; include last_modified when selecting the current or historical metadata state.
SELECT
    "id",
    "reading_type",
    "monitoring_location_id",
    "parameter_code",
    "parameter_name",
    "parameter_description",
    CAST("begin" AS TIMESTAMP) AS begin,
    CAST("end" AS TIMESTAMP) AS end,
    "last_modified",
    CAST("_lon" AS DOUBLE) AS lon,
    CAST("_lat" AS DOUBLE) AS lat
FROM "usgs-field-measurements-metadata"
