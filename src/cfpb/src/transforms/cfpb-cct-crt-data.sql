-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Market values identify product markets; compare or aggregate only after choosing the intended market.
SELECT
    "month",
    strptime("date", '%Y-%m')::DATE AS date,
    "tightness_index",
    "unadjusted_credit_tightness_index",
    "market"
FROM "cfpb-cct-crt-data"
