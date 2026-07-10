-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "s_adj",
    "bop_item",
    "sector10",
    "sectpart",
    "stk_flow",
    "partner",
    "currency",
    "geo",
    strptime("time_period", '%Y-%m')::DATE AS time_period,
    "value",
    "flag"
FROM "eurostat-teibp020"
