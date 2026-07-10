-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("gemeinde" AS VARCHAR) AS "gemeinde",
    CAST("belegungsart" AS VARCHAR) AS "belegungsart",
    CAST("anzahl_zimmer" AS VARCHAR) AS "anzahl_zimmer",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0902020100-136"
