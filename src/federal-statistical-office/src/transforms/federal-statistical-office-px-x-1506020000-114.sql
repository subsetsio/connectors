-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("jahr" AS VARCHAR) AS "jahr",
    CAST("form_des_ausbildungsbeitrags" AS VARCHAR) AS "form_des_ausbildungsbeitrags",
    CAST("kanton" AS VARCHAR) AS "kanton",
    CAST("bildungsstufe" AS VARCHAR) AS "bildungsstufe",
    CAST("betrag_und_bezügerinnen_und_bezüger" AS VARCHAR) AS "betrag_und_bezügerinnen_und_bezüger",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1506020000-114"
