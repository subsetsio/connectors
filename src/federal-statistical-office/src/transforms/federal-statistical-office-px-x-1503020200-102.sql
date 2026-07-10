-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("schwerpunktfach" AS VARCHAR) AS "schwerpunktfach",
    CAST("schulkanton" AS VARCHAR) AS "schulkanton",
    CAST("wohnkanton" AS VARCHAR) AS "wohnkanton",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1503020200-102"
