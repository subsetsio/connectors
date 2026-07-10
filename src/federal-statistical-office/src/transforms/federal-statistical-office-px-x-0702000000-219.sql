-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("bodenbedeckung_im_winter_und_bodenbearbeitung" AS VARCHAR) AS "bodenbedeckung_im_winter_und_bodenbearbeitung",
    CAST("einheit" AS VARCHAR) AS "einheit",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-219"
