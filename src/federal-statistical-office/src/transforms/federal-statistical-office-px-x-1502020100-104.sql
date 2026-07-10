-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("bildungstyp" AS VARCHAR) AS "bildungstyp",
    CAST("ausbildungsfeld" AS VARCHAR) AS "ausbildungsfeld",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502020100-104"
