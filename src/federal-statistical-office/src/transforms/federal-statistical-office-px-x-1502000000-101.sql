-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("degré_de_formation" AS VARCHAR) AS "degré_de_formation",
    CAST("canton_de_l_école" AS VARCHAR) AS "canton_de_l_école",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("nationalité_catégorie" AS VARCHAR) AS "nationalité_catégorie",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502000000-101"
