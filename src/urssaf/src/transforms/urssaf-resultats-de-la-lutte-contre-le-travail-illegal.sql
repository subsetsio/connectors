-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "type_d_action",
    "organisme",
    "region",
    "ancienne_region",
    "code_region",
    "code_ancienne_region",
    "nombre_actions",
    "nombre_redressements",
    "montant_redressements",
    "date_timestamp"
FROM "urssaf-resultats-de-la-lutte-contre-le-travail-illegal"
