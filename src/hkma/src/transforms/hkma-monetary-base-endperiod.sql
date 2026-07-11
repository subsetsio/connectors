-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "cert_of_indebt",
    "gov_notes_coins_circulation",
    "aggr_balance_bf_disc_win",
    "outstanding_efbn",
    "ow_lb_bf_disc_win",
    "mb_bf_disc_win_total"
FROM "hkma-monetary-base-endperiod"
