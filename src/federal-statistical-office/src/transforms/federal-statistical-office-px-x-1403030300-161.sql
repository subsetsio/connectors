-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("language_region" AS VARCHAR) AS "language_region",
    CAST("cancer_site" AS VARCHAR) AS "cancer_site",
    CAST("sex" AS VARCHAR) AS "sex",
    CAST("period" AS VARCHAR) AS "period",
    CAST("age_class" AS VARCHAR) AS "age_class",
    CAST("indicator" AS VARCHAR) AS "indicator",
    CAST("measure" AS VARCHAR) AS "measure",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1403030300-161"
