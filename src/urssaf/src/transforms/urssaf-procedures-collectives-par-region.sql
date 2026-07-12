-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "ancienne_region",
    "nature_de_procedure",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "code_region",
    "code_ancienne_region",
    "nombre_de_procedures_brut"
FROM "urssaf-procedures-collectives-par-region"
