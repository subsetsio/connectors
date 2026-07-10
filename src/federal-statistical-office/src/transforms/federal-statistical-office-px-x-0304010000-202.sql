-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("grande_région" AS VARCHAR) AS "grande_région",
    CAST("formation" AS VARCHAR) AS "formation",
    CAST("position_professionnelle" AS VARCHAR) AS "position_professionnelle",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("valeur_centrale_et_autres_percentiles" AS VARCHAR) AS "valeur_centrale_et_autres_percentiles",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0304010000-202"
