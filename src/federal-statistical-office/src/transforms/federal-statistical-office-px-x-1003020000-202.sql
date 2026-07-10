-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("monat" AS VARCHAR) AS "monat",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("indikator" AS VARCHAR) AS "indikator",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1003020000-202"
