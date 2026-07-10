-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("beobachtungseinheit" AS VARCHAR) AS "beobachtungseinheit",
    CAST("el_stelle" AS VARCHAR) AS "el_stelle",
    CAST("staatsangehörigkeit_kategorie" AS VARCHAR) AS "staatsangehörigkeit_kategorie",
    CAST("wohnsituation" AS VARCHAR) AS "wohnsituation",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1305020000-101"
