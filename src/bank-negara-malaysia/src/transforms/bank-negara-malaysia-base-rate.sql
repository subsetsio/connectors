-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bank_code",
    "bank_name",
    "base_rate",
    "base_lending_rate",
    "indicative_eff_lending_rate",
    "effective_date",
    "base_financing_rate"
FROM "bank-negara-malaysia-base-rate"
