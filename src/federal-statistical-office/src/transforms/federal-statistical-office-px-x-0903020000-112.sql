-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("anzahl_zimmer" AS VARCHAR) AS "anzahl_zimmer",
    CAST("belegungsart" AS VARCHAR) AS "belegungsart",
    CAST("bewohnertyp" AS VARCHAR) AS "bewohnertyp",
    CAST("gebäudekategorie" AS VARCHAR) AS "gebäudekategorie",
    CAST("hauseigentümertyp" AS VARCHAR) AS "hauseigentümertyp",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0903020000-112"
