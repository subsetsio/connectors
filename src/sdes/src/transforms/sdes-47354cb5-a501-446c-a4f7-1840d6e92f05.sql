-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "COMMUNE_CODE" AS commune_code,
    "COMMUNE_NOM" AS commune_nom,
    "CARBURANT" AS carburant,
    "STATUT_UTILISATEUR" AS statut_utilisateur,
    "GROUPE" AS groupe,
    "CATEGORIE" AS categorie,
    "IMMAT_2010" AS immat_2010,
    "IMMAT_2011" AS immat_2011,
    "IMMAT_2012" AS immat_2012,
    "IMMAT_2013" AS immat_2013,
    "IMMAT_2014" AS immat_2014,
    "IMMAT_2015" AS immat_2015,
    "IMMAT_2016" AS immat_2016,
    "IMMAT_2017" AS immat_2017,
    "IMMAT_2018" AS immat_2018,
    "IMMAT_2019" AS immat_2019,
    "IMMAT_2020" AS immat_2020,
    "IMMAT_2021" AS immat_2021,
    "IMMAT_2022" AS immat_2022,
    "IMMAT_2023" AS immat_2023,
    "IMMAT_2024" AS immat_2024,
    "IMMAT_2025" AS immat_2025
FROM "sdes-47354cb5-a501-446c-a4f7-1840d6e92f05"
