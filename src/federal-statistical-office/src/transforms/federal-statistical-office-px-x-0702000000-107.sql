-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("landwirtschaftliche_produktionszone" AS VARCHAR) AS "landwirtschaftliche_produktionszone",
    CAST("betriebssystem" AS VARCHAR) AS "betriebssystem",
    CAST("betriebsform" AS VARCHAR) AS "betriebsform",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-107"
