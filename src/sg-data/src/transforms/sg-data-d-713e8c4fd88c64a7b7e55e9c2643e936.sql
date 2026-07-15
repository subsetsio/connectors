-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vacc_date",
    "received_at_least_one_dose",
    "full_regimen",
    "minimum_protection",
    "received_one_dose_pcttakeup",
    "full_regimen_pcttakeup",
    "minimum_protection_pcttakeup"
FROM "sg-data-d-713e8c4fd88c64a7b7e55e9c2643e936"
