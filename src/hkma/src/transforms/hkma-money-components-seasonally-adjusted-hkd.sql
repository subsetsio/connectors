-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "legal_tender_notes_coins_in_pub",
    "demand_deposits_with_lb",
    "m1_supply"
FROM "hkma-money-components-seasonally-adjusted-hkd"
