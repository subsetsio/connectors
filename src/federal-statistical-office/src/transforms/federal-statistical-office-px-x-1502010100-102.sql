-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unterrichtsart" AS VARCHAR) AS "unterrichtsart",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("charakter_der_schule" AS VARCHAR) AS "charakter_der_schule",
    CAST("sonderpädagogische_massnahmen" AS VARCHAR) AS "sonderpädagogische_massnahmen",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502010100-102"
