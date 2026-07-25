-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "port_name",
    "state",
    "port_code",
    "border",
    CAST("date" AS TIMESTAMP) AS date,
    "measure",
    CAST("value" AS BIGINT) AS value,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "point"
FROM "u-s-department-of-transportation-keg4-3bc2"
