-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("ville_agglomération" AS VARCHAR) AS "ville_agglomération",
    CAST("indicateur_du_revenu_et_du_travail" AS VARCHAR) AS "indicateur_du_revenu_et_du_travail",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("résultat" AS VARCHAR) AS "résultat",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-2105000000-203"
