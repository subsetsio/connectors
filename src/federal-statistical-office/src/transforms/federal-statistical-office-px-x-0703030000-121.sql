-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("forstzone" AS VARCHAR) AS "forstzone",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0703030000-121"
