-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "type_d_organismes_complementaires",
    "type_de_contrats",
    "montant",
    "code_poste",
    "poste_niveau_1",
    "poste_niveau_2",
    "poste_niveau_3",
    "poste_niveau_4",
    "definition_du_poste"
FROM "drees-organismes-complementaires-comptes-detailles"
