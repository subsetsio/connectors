-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "commodity",
    CAST("east" AS BIGINT) AS east,
    CAST("great_lakes" AS BIGINT) AS great_lakes,
    CAST("gulf" AS BIGINT) AS gulf,
    CAST("west" AS BIGINT) AS west
FROM "u-s-department-of-transportation-yirh-jy8u"
