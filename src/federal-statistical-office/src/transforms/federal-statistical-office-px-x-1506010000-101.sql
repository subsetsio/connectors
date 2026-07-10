-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("verwaltungsebene" AS VARCHAR) AS "verwaltungsebene",
    CAST("bildungsstufe" AS VARCHAR) AS "bildungsstufe",
    CAST("ausgabenart" AS VARCHAR) AS "ausgabenart",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506010000-101"
