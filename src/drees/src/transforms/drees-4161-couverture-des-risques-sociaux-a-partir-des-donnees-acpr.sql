-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "type_d_organismes_complementaires",
    "type_de_contrats",
    "montant",
    "cotisations_prestations",
    "code_risque",
    "niveau_du_risque",
    "risque_niveau_1",
    "risque_niveau_2",
    "risque_niveau_3",
    "risque_niveau_4",
    "risque_niveau_5",
    "risque_niveau_6",
    "definition_du_risque"
FROM "drees-4161-couverture-des-risques-sociaux-a-partir-des-donnees-acpr"
