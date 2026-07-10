-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("höchste_abgeschlossene_ausbildung" AS VARCHAR) AS "höchste_abgeschlossene_ausbildung",
    CAST("kanton_bezirk_gemeinde" AS VARCHAR) AS "kanton_bezirk_gemeinde",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-4003000000-161"
