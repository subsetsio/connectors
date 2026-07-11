-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "effect_date",
    "dr_1w",
    "dr_1m",
    "dr_3m",
    "dr_6m",
    "dr_12m",
    "savings_deposit_rate",
    "best_lending_rate"
FROM "hkma-hkd-interest-rates-effective"
