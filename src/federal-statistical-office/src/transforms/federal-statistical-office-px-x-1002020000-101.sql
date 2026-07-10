-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("indicator" AS VARCHAR) AS "indicator",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("product" AS VARCHAR) AS "product",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1002020000-101"
