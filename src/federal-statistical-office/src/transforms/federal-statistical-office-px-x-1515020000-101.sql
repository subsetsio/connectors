-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("type_de_dépense" AS VARCHAR) AS "type_de_dépense",
    CAST("unité_de_mesure" AS VARCHAR) AS "unité_de_mesure",
    CAST("département_de_la_confédération" AS VARCHAR) AS "département_de_la_confédération",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1515020000-101"
