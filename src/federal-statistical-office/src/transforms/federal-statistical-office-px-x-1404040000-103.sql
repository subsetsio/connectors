-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("leistungserbringertyp" AS VARCHAR) AS "leistungserbringertyp",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("ausbildung_hauptfunktion" AS VARCHAR) AS "ausbildung_hauptfunktion",
    CAST("personal" AS VARCHAR) AS "personal",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1404040000-103"
