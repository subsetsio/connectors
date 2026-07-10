-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("typologie_urbain_rural" AS VARCHAR) AS "typologie_urbain_rural",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("résultat" AS VARCHAR) AS "résultat",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-2105000000-404"
