-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("poste_comptable" AS VARCHAR) AS "poste_comptable",
    CAST("canton" AS VARCHAR) AS "canton",
    CAST("branche_du_secteur_primaire" AS VARCHAR) AS "branche_du_secteur_primaire",
    CAST("secteur_institutionnel" AS VARCHAR) AS "secteur_institutionnel",
    CAST("unité" AS VARCHAR) AS "unité",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-0704050000-102"
