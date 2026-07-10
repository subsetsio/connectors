-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("wirtschaftsabteilung" AS VARCHAR) AS "wirtschaftsabteilung",
    CAST("grössenklasse" AS VARCHAR) AS "grössenklasse",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0602050000-102"
