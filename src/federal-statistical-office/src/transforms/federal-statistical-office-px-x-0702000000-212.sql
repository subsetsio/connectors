-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("année" AS VARCHAR) AS "année",
    CAST("classe_de_taille_sau" AS VARCHAR) AS "classe_de_taille_sau",
    CAST("type_de_main_d_oeuvre" AS VARCHAR) AS "type_de_main_d_oeuvre",
    CAST("sexe" AS VARCHAR) AS "sexe",
    CAST("activité" AS VARCHAR) AS "activité",
    CAST("résultat" AS VARCHAR) AS "résultat",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0702000000-212"
