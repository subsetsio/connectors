-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "port",
    "bridge",
    CAST("air_draft_in_feet" AS BIGINT) AS air_draft_in_feet
FROM "u-s-department-of-transportation-25e5-bvnb"
