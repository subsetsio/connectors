-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("scénario" AS VARCHAR) AS "scénario",
    CAST("haute_école" AS VARCHAR) AS "haute_école",
    CAST("domaine_d_études" AS VARCHAR) AS "domaine_d_études",
    CAST("niveau" AS VARCHAR) AS "niveau",
    CAST("certificat_d_accès" AS VARCHAR) AS "certificat_d_accès",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("année" AS VARCHAR) AS "année",
    CAST("unité_d_observation" AS VARCHAR) AS "unité_d_observation",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1509090000-112"
