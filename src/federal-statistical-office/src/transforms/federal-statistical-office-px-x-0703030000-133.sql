-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "forest_zone",
    "priority_function",
    CAST("year" AS BIGINT) AS year,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0703030000-133"
