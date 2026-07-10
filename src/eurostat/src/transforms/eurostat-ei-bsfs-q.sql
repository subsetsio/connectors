-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "s_adj",
    "nace_r2",
    "indic",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-ei-bsfs-q"
