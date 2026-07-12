-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "organisme",
    "region",
    "ancienne_region",
    "code_region",
    "code_ancienne_region",
    "categorie_cotisant",
    "comptes_cotisants",
    "date_timestamp"
FROM "urssaf-denombrement-annuel-des-comptes-cotisants-urssaf"
