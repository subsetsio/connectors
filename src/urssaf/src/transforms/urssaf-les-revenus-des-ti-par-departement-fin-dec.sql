-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_de_travailleur_independant",
    "region",
    "ancienne_region",
    "departement",
    "annee",
    "code_region",
    "code_ancienne_region",
    "code_departement",
    "nombre_de_ti",
    "revenu"
FROM "urssaf-les-revenus-des-ti-par-departement-fin-dec"
