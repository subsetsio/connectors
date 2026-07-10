-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("aufwandsart" AS VARCHAR) AS "aufwandsart",
    CAST("masseinheit" AS VARCHAR) AS "masseinheit",
    CAST("empfängerstelle" AS VARCHAR) AS "empfängerstelle",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1515020000-102"
