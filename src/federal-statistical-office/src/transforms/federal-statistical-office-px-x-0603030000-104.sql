-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("adjustment" AS VARCHAR) AS "adjustment",
    CAST("indices_changes" AS VARCHAR) AS "indices_changes",
    CAST("turnover" AS VARCHAR) AS "turnover",
    CAST("branch" AS VARCHAR) AS "branch",
    CAST("year" AS VARCHAR) AS "year",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0603030000-104"
