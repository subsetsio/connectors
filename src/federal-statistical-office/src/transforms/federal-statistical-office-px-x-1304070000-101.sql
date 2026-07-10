-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("leistungsart" AS VARCHAR) AS "leistungsart",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("jahr_des_leistungsanspruchs" AS VARCHAR) AS "jahr_des_leistungsanspruchs",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304070000-101"
