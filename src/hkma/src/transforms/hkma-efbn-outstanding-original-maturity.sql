-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "efb_91d",
    "efb_182d",
    "efb_364d",
    "efb",
    "efn",
    "efbn_total"
FROM "hkma-efbn-outstanding-original-maturity"
