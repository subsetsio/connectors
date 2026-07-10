-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("ville_agglomération" AS VARCHAR) AS "ville_agglomération",
    CAST("indicateurs_de_culture_et_de_loisirs" AS VARCHAR) AS "indicateurs_de_culture_et_de_loisirs",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-2105000000-205"
