-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_quarter",
    "endperiod_noofaccts",
    "endperiod_delinquent_amt",
    "during_chargeoff_amt",
    "during_rollover_amt",
    "during_avg_total_receivables"
FROM "hkma-credit-card-lending-survey"
