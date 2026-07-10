-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST("zivilstand" AS VARCHAR) AS "zivilstand",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("absolut_relativ" AS VARCHAR) AS "absolut_relativ",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304030000-121"
