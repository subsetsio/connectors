-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "commodity",
    CAST("east" AS DOUBLE) AS east,
    CAST("great_lakes" AS DOUBLE) AS great_lakes,
    CAST("gulf" AS DOUBLE) AS gulf,
    CAST("west" AS DOUBLE) AS west
FROM "u-s-department-of-transportation-vpgu-kvxj"
