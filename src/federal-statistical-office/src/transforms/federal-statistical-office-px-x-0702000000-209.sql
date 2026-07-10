-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("classe_de_taille_sau" AS VARCHAR) AS "classe_de_taille_sau",
    CAST("gestion_formation_condition_de_propriété_et_reprise" AS VARCHAR) AS "gestion_formation_condition_de_propriété_et_reprise",
    CAST("unité_d_observation" AS VARCHAR) AS "unité_d_observation",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-209"
