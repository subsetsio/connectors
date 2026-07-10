-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("investment" AS VARCHAR) AS "investment",
    CAST("forest_zone" AS VARCHAR) AS "forest_zone",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0703030000-135"
