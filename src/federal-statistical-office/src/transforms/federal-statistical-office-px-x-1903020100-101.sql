-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("offence" AS VARCHAR) AS "offence",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("level_of_completion" AS VARCHAR) AS "level_of_completion",
    CAST("level_of_detection" AS VARCHAR) AS "level_of_detection",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1903020100-101"
