-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("masseinheit" AS VARCHAR) AS "masseinheit",
    CAST("land" AS VARCHAR) AS "land",
    CAST("ausgabenart" AS VARCHAR) AS "ausgabenart",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1302020000-101"
