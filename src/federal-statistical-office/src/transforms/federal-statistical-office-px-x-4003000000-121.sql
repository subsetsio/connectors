-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("wohnsitztyp" AS VARCHAR) AS "wohnsitztyp",
    CAST("kanton_bezirk_gemeinde" AS VARCHAR) AS "kanton_bezirk_gemeinde",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("zivilstand" AS VARCHAR) AS "zivilstand",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-4003000000-121"
