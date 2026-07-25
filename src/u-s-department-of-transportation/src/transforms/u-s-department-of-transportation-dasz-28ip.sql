-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "port",
    "bridge",
    CAST("air_draft_in_feet" AS BIGINT) AS air_draft_in_feet
FROM "u-s-department-of-transportation-dasz-28ip"
