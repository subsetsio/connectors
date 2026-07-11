-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "transinhk_plcmt_brwg",
    "transinhk_swap",
    "transinhk_total",
    "transouthk_plcmt_brwg",
    "transouthk_swap",
    "transouthk_total",
    "alltrans_plcmt_brwg",
    "alltrans_swap",
    "alltrans_total"
FROM "hkma-hkd-interbank-transactions"
