-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "category",
    "type",
    CAST("vehicles" AS BIGINT) AS vehicles
FROM "u-s-department-of-transportation-4dra-vxq7"
