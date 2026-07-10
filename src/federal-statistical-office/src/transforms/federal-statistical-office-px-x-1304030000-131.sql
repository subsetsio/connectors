-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("classe_d_âge" AS VARCHAR) AS "classe_d_âge",
    CAST("formation" AS VARCHAR) AS "formation",
    CAST("situation_d_activité" AS VARCHAR) AS "situation_d_activité",
    CAST("nationalité_catégorie" AS VARCHAR) AS "nationalité_catégorie",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304030000-131"
