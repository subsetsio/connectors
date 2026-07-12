-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "type_action",
    "organisme",
    "region",
    "ancienne_region",
    "code_region",
    "code_ancienne_region",
    "nombre_actions",
    "nombre_de_regularisations",
    "montant_redressements",
    "montant_restitutions",
    "montant_regularisations",
    "date_timestamp"
FROM "urssaf-resultats-du-controle-par-les-urssaf"
