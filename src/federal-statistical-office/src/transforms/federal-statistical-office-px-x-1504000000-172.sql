-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("schuljahr" AS VARCHAR) AS "schuljahr",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("bildungsstufe" AS VARCHAR) AS "bildungsstufe",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1504000000-172"
