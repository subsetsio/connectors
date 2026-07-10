-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("ausbildungsfeld" AS VARCHAR) AS "ausbildungsfeld",
    CAST("lehrbetriebskanton" AS VARCHAR) AS "lehrbetriebskanton",
    CAST("ausbildungstyp" AS VARCHAR) AS "ausbildungstyp",
    CAST("ausbildungsform" AS VARCHAR) AS "ausbildungsform",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502020100-203"
