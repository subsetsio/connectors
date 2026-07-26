-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mwbe_type",
    "prime_contracts_professional_services",
    "prime_contracts_standard_services",
    "prime_contracts_goods",
    "prime_contracts_construction",
    "subcontracts_professional_services",
    "subcontracts_construction"
FROM "nyc-open-data-svyi-maaj"
