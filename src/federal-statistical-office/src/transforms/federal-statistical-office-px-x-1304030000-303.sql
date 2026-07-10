-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("struktur_der_unterstützungseinheit" AS VARCHAR) AS "struktur_der_unterstützungseinheit",
    CAST("bezugsdauer" AS VARCHAR) AS "bezugsdauer",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304030000-303"
