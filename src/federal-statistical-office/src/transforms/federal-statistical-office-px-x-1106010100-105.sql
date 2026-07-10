-- provisional pass-through for PxWeb cube; regenerate from the settled model after model-verify.
SELECT
    CAST("genre_d_objet_genre_d_usager" AS VARCHAR) AS "genre_d_objet_genre_d_usager",
    CAST("responsabilité_présumée_de_l_objet" AS VARCHAR) AS "responsabilité_présumée_de_l_objet",
    CAST("sexe_du_piéton_ou_du_conducteur" AS VARCHAR) AS "sexe_du_piéton_ou_du_conducteur",
    CAST("classe_d_âge_du_piéton_ou_du_conducteur" AS VARCHAR) AS "classe_d_âge_du_piéton_ou_du_conducteur",
    CAST("ancienneté_du_permis_de_conduire_du_conducteur" AS VARCHAR) AS "ancienneté_du_permis_de_conduire_du_conducteur",
    CAST("gravité_de_l_accident" AS VARCHAR) AS "gravité_de_l_accident",
    CAST("année" AS VARCHAR) AS "année",
    CAST(value AS DOUBLE) AS value,
    CAST(cube_id AS VARCHAR) AS cube_id,
    CAST(updated AS VARCHAR) AS updated
FROM "federal-statistical-office-px-x-1106010100-105"
