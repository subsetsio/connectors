-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("anzahl_zimmer" AS VARCHAR) AS "anzahl_zimmer",
    CAST("belegungsart" AS VARCHAR) AS "belegungsart",
    CAST("bewohnertyp" AS VARCHAR) AS "bewohnertyp",
    CAST("mietpreisklasse" AS VARCHAR) AS "mietpreisklasse",
    CAST("wohnungsfläche" AS VARCHAR) AS "wohnungsfläche",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0903020000-111"
