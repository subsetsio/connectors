-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("district_commune" AS VARCHAR) AS "district_commune",
    CAST("année" AS VARCHAR) AS "année",
    CAST("parti" AS VARCHAR) AS "parti",
    CAST("résultats" AS VARCHAR) AS "résultats",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1702020000-105"
