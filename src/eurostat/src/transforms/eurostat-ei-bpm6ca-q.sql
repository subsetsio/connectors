-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "unit",
    "s_adj",
    "sector10",
    "sectpart",
    "partner",
    "stk_flow",
    "bop_item",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-ei-bpm6ca-q"
