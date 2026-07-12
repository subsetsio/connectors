-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "departement",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "code_region",
    "code_departement",
    "immatriculations",
    "radiations",
    "chiffres_d_affaires",
    "economiquement_actifs",
    "administrativement_actifs"
FROM "urssaf-auto-entrepreneurs-par-departement"
