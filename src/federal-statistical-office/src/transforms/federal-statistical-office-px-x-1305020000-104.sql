-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unité_d_observation" AS VARCHAR) AS "unité_d_observation",
    CAST("office_pc" AS VARCHAR) AS "office_pc",
    CAST("nationalité_catégorie" AS VARCHAR) AS "nationalité_catégorie",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1305020000-104"
