-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("masseinheit" AS VARCHAR) AS "masseinheit",
    CAST("bereich_des_agrarsektors" AS VARCHAR) AS "bereich_des_agrarsektors",
    CAST("bewertungsmethode" AS VARCHAR) AS "bewertungsmethode",
    CAST("kontoposten" AS VARCHAR) AS "kontoposten",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0704000000-121"
