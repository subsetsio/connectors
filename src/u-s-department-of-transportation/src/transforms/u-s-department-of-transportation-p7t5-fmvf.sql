-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "commodity",
    CAST("east" AS BIGINT) AS east,
    CAST("great_lakes" AS BIGINT) AS great_lakes,
    CAST("gulf" AS BIGINT) AS gulf,
    CAST("west" AS BIGINT) AS west
FROM "u-s-department-of-transportation-p7t5-fmvf"
