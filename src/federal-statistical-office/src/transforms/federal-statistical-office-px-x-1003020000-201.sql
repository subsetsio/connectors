-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("year" AS VARCHAR) AS "year",
    CAST("month" AS VARCHAR) AS "month",
    CAST("commune" AS VARCHAR) AS "commune",
    CAST("indicator" AS VARCHAR) AS "indicator",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1003020000-201"
