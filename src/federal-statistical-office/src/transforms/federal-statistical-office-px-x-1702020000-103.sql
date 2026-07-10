-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("année" AS VARCHAR) AS "année",
    CAST("parti" AS VARCHAR) AS "parti",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("résultats" AS VARCHAR) AS "résultats",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1702020000-103"
