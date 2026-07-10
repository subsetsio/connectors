-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("kanton_bezirk_gemeinde" AS VARCHAR) AS "kanton_bezirk_gemeinde",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("höchste_abgeschlossene_ausbildung" AS VARCHAR) AS "höchste_abgeschlossene_ausbildung",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-4002000000-161"
