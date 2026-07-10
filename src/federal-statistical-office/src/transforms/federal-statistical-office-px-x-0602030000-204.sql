-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unité_d_observation" AS VARCHAR) AS "unité_d_observation",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("secteur_économique" AS VARCHAR) AS "secteur_économique",
    CAST("classe_de_taille" AS VARCHAR) AS "classe_de_taille",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0602030000-204"
