-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton_communes" AS VARCHAR) AS "canton_communes",
    CAST("year" AS VARCHAR) AS "year",
    CAST("cinema_type" AS VARCHAR) AS "cinema_type",
    CAST("infrastructure" AS VARCHAR) AS "infrastructure",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1602010000-101"
