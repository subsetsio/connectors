-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("niveau_d_examen" AS VARCHAR) AS "niveau_d_examen",
    CAST("branche_d_études" AS VARCHAR) AS "branche_d_études",
    CAST("nationalité_catégorie" AS VARCHAR) AS "nationalité_catégorie",
    CAST("haute_école" AS VARCHAR) AS "haute_école",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1503040100-102"
