-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("canton_de_l_école" AS VARCHAR) AS "canton_de_l_école",
    CAST("forme_d_enseignement" AS VARCHAR) AS "forme_d_enseignement",
    CAST("mesures_de_pédagogie_spécialisée" AS VARCHAR) AS "mesures_de_pédagogie_spécialisée",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502010100-101"
