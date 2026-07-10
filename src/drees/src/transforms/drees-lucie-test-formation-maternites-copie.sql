-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "id_mat",
    "nom_mat",
    "type",
    "statut",
    "fi_et",
    "fi_ej",
    "com",
    "nomcom",
    "cpo",
    "adresse",
    "lit_obs",
    "saltrav",
    "acctot",
    "suivi",
    "point_geo_" AS point_geo,
    "nom_departement",
    "region",
    CAST("code_region" AS BIGINT) AS code_region,
    "forme_departement",
    "forme_geo",
    "code_departement",
    "dep_pop_tot",
    "nombre_de_naissances_vivantes_domiciliees_en_2022"
FROM "drees-lucie-test-formation-maternites-copie"
