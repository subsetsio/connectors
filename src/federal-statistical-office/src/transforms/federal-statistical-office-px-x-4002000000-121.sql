-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("canton_district_commune" AS VARCHAR) AS "canton_district_commune",
    CAST("nationalité_catégorie" AS VARCHAR) AS "nationalité_catégorie",
    CAST("langue_principale" AS VARCHAR) AS "langue_principale",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-4002000000-121"
