-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("domaine_d_études" AS VARCHAR) AS "domaine_d_études",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("haute_école" AS VARCHAR) AS "haute_école",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1502040200-181"
