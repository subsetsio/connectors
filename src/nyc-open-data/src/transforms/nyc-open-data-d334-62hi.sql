-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "issuer",
    "transaction_number_and_type",
    "counterparty",
    "notional_amount",
    "trade_date",
    "termination_date",
    "mark_to_market_value",
    "data_as_of"
FROM "nyc-open-data-d334-62hi"
