-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "s_adj",
    "age",
    "unit",
    "sex",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-une-rt-q-h"
