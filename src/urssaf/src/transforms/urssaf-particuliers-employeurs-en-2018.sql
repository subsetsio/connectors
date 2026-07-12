-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_categorie_d_emploi",
    "categorie_d_emploi",
    "ancienne_region",
    "region",
    "departement",
    "code_ancienne_region",
    "code_region",
    "code_departement",
    "nombre_d_employeurs",
    "nombre_d_heures_declarees",
    "masse_salariale_nette",
    "nombre_de_mois_de_declarations",
    "somme_des_ages",
    "age_moyen_categ_x_dep",
    "geom",
    "geo_point_2d"
FROM "urssaf-particuliers-employeurs-en-2018"
