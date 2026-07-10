-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année_scolaire" AS VARCHAR) AS "année_scolaire",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("taux_d_occupation" AS VARCHAR) AS "taux_d_occupation",
    CAST("degré_de_formation" AS VARCHAR) AS "degré_de_formation",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1504000000-173"
