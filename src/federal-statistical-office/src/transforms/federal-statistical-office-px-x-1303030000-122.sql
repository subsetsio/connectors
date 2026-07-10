-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("unité_d_observation" AS VARCHAR) AS "unité_d_observation",
    CAST("forme_administrative" AS VARCHAR) AS "forme_administrative",
    CAST("genre_de_couverture_des_risques" AS VARCHAR) AS "genre_de_couverture_des_risques",
    CAST("forme_juridique" AS VARCHAR) AS "forme_juridique",
    CAST("enregistrement_ip" AS VARCHAR) AS "enregistrement_ip",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1303030000-122"
