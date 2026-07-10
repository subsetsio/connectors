-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("typ_der_arbeitskraft" AS VARCHAR) AS "typ_der_arbeitskraft",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("erwerbstätigkeit" AS VARCHAR) AS "erwerbstätigkeit",
    CAST("resultat" AS VARCHAR) AS "resultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-210"
