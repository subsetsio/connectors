-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("leistung" AS VARCHAR) AS "leistung",
    CAST("geldgeber" AS VARCHAR) AS "geldgeber",
    CAST("hochschule" AS VARCHAR) AS "hochschule",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506030300-261"
