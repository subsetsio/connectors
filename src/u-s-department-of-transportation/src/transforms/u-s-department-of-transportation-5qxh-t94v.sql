-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "state",
    CAST("year" AS BIGINT) AS year,
    "month",
    CAST("vol_gasoline" AS BIGINT) AS vol_gasoline,
    "data_type",
    CAST("date_modified" AS TIMESTAMP) AS date_modified
FROM "u-s-department-of-transportation-5qxh-t94v"
