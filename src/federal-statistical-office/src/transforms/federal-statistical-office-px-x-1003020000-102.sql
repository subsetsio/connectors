-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("month" AS VARCHAR) AS "month",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("visitors_country_of_residence" AS VARCHAR) AS "visitors_country_of_residence",
    CAST("indicator" AS VARCHAR) AS "indicator",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1003020000-102"
