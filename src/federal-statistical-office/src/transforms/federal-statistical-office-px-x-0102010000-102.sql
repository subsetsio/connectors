-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("population_type" AS VARCHAR) AS "population_type",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("marital_status" AS VARCHAR) AS "marital_status",
    CAST("age" AS VARCHAR) AS "age",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102010000-102"
