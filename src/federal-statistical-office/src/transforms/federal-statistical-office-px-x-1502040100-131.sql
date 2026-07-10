-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("isced_field" AS VARCHAR) AS "isced_field",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("level_of_study" AS VARCHAR) AS "level_of_study",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502040100-131"
