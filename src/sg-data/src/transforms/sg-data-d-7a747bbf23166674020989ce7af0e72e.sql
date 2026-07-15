-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cards_main",
    "cards_supplementary",
    "total_billings",
    "rollover_balance",
    "bad_debts_written_off",
    "charge_off_rates"
FROM "sg-data-d-7a747bbf23166674020989ce7af0e72e"
