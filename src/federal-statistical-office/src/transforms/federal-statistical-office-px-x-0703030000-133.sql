-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("indicator" AS VARCHAR) AS "indicator",
    CAST("forest_zone" AS VARCHAR) AS "forest_zone",
    CAST("priority_function" AS VARCHAR) AS "priority_function",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0703030000-133"
