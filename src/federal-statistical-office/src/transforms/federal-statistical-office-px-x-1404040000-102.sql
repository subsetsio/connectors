-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("leistungserbringertyp" AS VARCHAR) AS "leistungserbringertyp",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("leistungsangebot" AS VARCHAR) AS "leistungsangebot",
    CAST("klienten_und_leistungen" AS VARCHAR) AS "klienten_und_leistungen",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1404040000-102"
