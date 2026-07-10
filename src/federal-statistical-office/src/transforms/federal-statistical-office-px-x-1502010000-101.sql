-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("education_level" AS VARCHAR) AS "education_level",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("citizenship_category" AS VARCHAR) AS "citizenship_category",
    CAST("first_language" AS VARCHAR) AS "first_language",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502010000-101"
