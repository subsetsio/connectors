-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "code_ancienne_region",
    "ancienne_region",
    "code_region",
    "region",
    "categorie_de_cotisants",
    "type_de_service",
    "note",
    "taux_de_satisfaction",
    "date_unix"
FROM "urssaf-resultats-des-enquetes-de-satisfaction"
