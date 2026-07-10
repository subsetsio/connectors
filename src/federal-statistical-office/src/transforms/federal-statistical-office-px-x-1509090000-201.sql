-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("szenario" AS VARCHAR) AS "szenario",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("bildungsniveau" AS VARCHAR) AS "bildungsniveau",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("variablen" AS VARCHAR) AS "variablen",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1509090000-201"
