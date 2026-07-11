-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "imp_exp_reexp_fromhk_hkd",
    "imp_exp_reexp_fromhk_fc",
    "imp_exp_reexp_fromhk_total",
    "merch_trade_nonhk_hkd",
    "merch_trade_nonhk_fc",
    "merch_trade_nonhk_total",
    "loans_inhk_hkd",
    "loans_inhk_fc",
    "loans_inhk_total",
    "other_loans_outhk_hkd",
    "other_loans_outhk_fc",
    "other_loans_outhk_total",
    "other_loans_unkplace_hkd",
    "other_loans_unkplace_fc",
    "other_loans_unkplace_total",
    "total_loans_hkd",
    "total_loans_fc",
    "total_loans"
FROM "hkma-loans-by-type-lb"
