-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kontoposten" AS VARCHAR) AS "kontoposten",
    CAST("branche_des_primärsektors" AS VARCHAR) AS "branche_des_primärsektors",
    CAST("institutioneller_sektor" AS VARCHAR) AS "institutioneller_sektor",
    CAST("masseinheit" AS VARCHAR) AS "masseinheit",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0704000000-101"
