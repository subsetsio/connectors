-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("mutmassliche_ursache" AS VARCHAR) AS "mutmassliche_ursache",
    CAST("objektart_verkehrsteilnahme" AS VARCHAR) AS "objektart_verkehrsteilnahme",
    CAST("strassenart" AS VARCHAR) AS "strassenart",
    CAST("unfallort" AS VARCHAR) AS "unfallort",
    CAST("unfallschwere" AS VARCHAR) AS "unfallschwere",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1106010100-106"
