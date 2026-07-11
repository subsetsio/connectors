-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "liquid_adj_fac_bid_rate",
    "disc_win_base_rate",
    "hibor_overnight",
    "hibor_fixing_1m",
    "liquid_adj_win_offer_rate"
FROM "hkma-discount-window-rates-endperiod"
