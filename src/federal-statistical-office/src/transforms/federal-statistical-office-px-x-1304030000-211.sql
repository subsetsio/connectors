-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("état_civil" AS VARCHAR) AS "état_civil",
    CAST("situation_d_activité" AS VARCHAR) AS "situation_d_activité",
    CAST("groupe_de_personnes" AS VARCHAR) AS "groupe_de_personnes",
    CAST("nationalité_catégorie" AS VARCHAR) AS "nationalité_catégorie",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304030000-211"
