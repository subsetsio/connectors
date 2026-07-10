-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "isco08",
    "nace_r2_1",
    "sizeclas",
    "s_adj",
    "indic_em",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-jvs-q-isco-r21"
