-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("statut_de_séjour" AS VARCHAR) AS "statut_de_séjour",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("classe_d_âge" AS VARCHAR) AS "classe_d_âge",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1304030000-133"
