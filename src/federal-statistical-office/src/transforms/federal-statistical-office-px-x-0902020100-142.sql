-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("gemeinde" AS VARCHAR) AS "gemeinde",
    CAST("anzahl_zimmer" AS VARCHAR) AS "anzahl_zimmer",
    CAST("wohnungsfläche" AS VARCHAR) AS "wohnungsfläche",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0902020100-142"
