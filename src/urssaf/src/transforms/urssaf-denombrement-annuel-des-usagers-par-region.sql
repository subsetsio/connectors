-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "region",
    "ancienne_region",
    "categorie_cotisant",
    "code_region",
    "code_ancienne_region",
    "comptes_cotisants",
    "date_timestamp"
FROM "urssaf-denombrement-annuel-des-usagers-par-region"
