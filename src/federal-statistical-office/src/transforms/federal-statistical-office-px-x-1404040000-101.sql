-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("leistungserbringertyp" AS VARCHAR) AS "leistungserbringertyp",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("leistungsangebot" AS VARCHAR) AS "leistungsangebot",
    CAST("leistungserbringer" AS VARCHAR) AS "leistungserbringer",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1404040000-101"
