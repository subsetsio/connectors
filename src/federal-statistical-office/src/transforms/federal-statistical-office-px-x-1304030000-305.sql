-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("aufenthaltsstatus" AS VARCHAR) AS "aufenthaltsstatus",
    CAST("geschlecht" AS VARCHAR) AS "geschlecht",
    CAST("altersklasse" AS VARCHAR) AS "altersklasse",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304030000-305"
