-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "spot_assets",
    "forward_purchases",
    "spot_liabilities",
    "forward_sales",
    "net_spot_position",
    "net_forward_position",
    "open_position"
FROM "hkma-fc-position-chf"
