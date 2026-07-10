-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("invaliditätsursache" AS VARCHAR) AS "invaliditätsursache",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1305010000-113"
