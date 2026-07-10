-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("region" AS VARCHAR) AS "region",
    CAST("innerbetriebliche_diversifikation_und_anteil_am_gesamtumsatz" AS VARCHAR) AS "innerbetriebliche_diversifikation_und_anteil_am_gesamtumsatz",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-205"
