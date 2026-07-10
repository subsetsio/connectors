-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("ausbildungstyp" AS VARCHAR) AS "ausbildungstyp",
    CAST("ausbildungsfeld" AS VARCHAR) AS "ausbildungsfeld",
    CAST("diplomtyp" AS VARCHAR) AS "diplomtyp",
    CAST("wohnkanton" AS VARCHAR) AS "wohnkanton",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1503030000-103"
