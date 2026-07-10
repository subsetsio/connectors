-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("région" AS VARCHAR) AS "région",
    CAST("digitalisation" AS VARCHAR) AS "digitalisation",
    CAST("résultat" AS VARCHAR) AS "résultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-262"
