-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("agglomeration" AS VARCHAR) AS "agglomeration",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-2105000000-401"
