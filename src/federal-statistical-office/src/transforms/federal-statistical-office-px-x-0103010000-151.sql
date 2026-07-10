-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("citizenship" AS VARCHAR) AS "citizenship",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("demographic_component" AS VARCHAR) AS "demographic_component",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0103010000-151"
