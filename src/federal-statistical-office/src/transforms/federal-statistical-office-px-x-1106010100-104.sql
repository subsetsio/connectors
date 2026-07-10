-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unfallfolge" AS VARCHAR) AS "unfallfolge",
    CAST("verwendetes_verkehrsmittel" AS VARCHAR) AS "verwendetes_verkehrsmittel",
    CAST("art_der_verkehrsteilnahme" AS VARCHAR) AS "art_der_verkehrsteilnahme",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST("verwendung_eines_schutzsystems" AS VARCHAR) AS "verwendung_eines_schutzsystems",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1106010100-104"
