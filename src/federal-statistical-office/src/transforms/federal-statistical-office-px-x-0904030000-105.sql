-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("grossregion_kanton_gemeinde" AS VARCHAR) AS "grossregion_kanton_gemeinde",
    CAST("anzahl_zimmer" AS VARCHAR) AS "anzahl_zimmer",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0904030000-105"
