-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "unit",
    "sex",
    "deg_urb",
    "age",
    "wstatus",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-lfsq-pgauws"
