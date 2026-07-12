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
    "nombre_de_salaries",
    "nombre_de_femmes_salariees",
    "nombre_d_hommes_salaries",
    "nombre_d_heures_declarees",
    "masse_salariale_nette",
    "nombre_de_relations_contract",
    "nombre_de_salaries_t4",
    "nombre_de_femmes_salariees_t4",
    "nombre_d_hommes_salaries_t4",
    "nombre_d_heures_declarees_t4",
    "masse_salariale_nette_t4",
    "nombre_de_relat_contract_t4",
    "somme_des_ages_t4",
    "age_moyen_au_t4_categ_x_dep",
    "geom",
    "geo_point_2d"
FROM "urssaf-salaries-des-particuliers-employeurs-en-2018"
