-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "organisme",
    "region",
    "ancienne_region",
    "categorie_encaissements",
    "categorie_encaissements_detaillee",
    "code_region",
    "code_ancienne_region",
    "montant_des_encaissements",
    "date_timestamp"
FROM "urssaf-encaissements-annuels-des-urssaf"
