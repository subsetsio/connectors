-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("niveau_d_examen" AS VARCHAR) AS "niveau_d_examen",
    CAST("canton_de_domicile_avant_le_début_des_études" AS VARCHAR) AS "canton_de_domicile_avant_le_début_des_études",
    CAST("haute_école" AS VARCHAR) AS "haute_école",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1503040200-113"
