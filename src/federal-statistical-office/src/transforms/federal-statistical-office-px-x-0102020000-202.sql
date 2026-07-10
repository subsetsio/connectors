-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("citizenship_category" AS VARCHAR) AS "citizenship_category",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("age" AS VARCHAR) AS "age",
    CAST("demographic_component" AS VARCHAR) AS "demographic_component",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102020000-202"
