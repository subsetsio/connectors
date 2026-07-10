-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "s_adj",
    "sectpart",
    "sector10",
    "bop_item",
    "stk_flow",
    "partner",
    "unit",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-tipsbp50"
