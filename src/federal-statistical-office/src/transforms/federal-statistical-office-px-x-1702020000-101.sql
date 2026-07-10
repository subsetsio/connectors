-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton_bezirk_gemeinde" AS VARCHAR) AS "kanton_bezirk_gemeinde",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("ergebnisse" AS VARCHAR) AS "ergebnisse",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1702020000-101"
