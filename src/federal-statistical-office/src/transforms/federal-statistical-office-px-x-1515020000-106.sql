-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("f_e_personalkategorie" AS VARCHAR) AS "f_e_personalkategorie",
    CAST("masseinheit" AS VARCHAR) AS "masseinheit",
    CAST("tätigkeit" AS VARCHAR) AS "tätigkeit",
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1515020000-106"
