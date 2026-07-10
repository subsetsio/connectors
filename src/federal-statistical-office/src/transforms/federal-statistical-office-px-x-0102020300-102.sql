-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("âge" AS VARCHAR) AS "âge",
    CAST("unité_d_observation" AS VARCHAR) AS "unité_d_observation",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0102020300-102"
