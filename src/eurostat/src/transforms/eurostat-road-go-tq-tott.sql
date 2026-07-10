-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "tra_type",
    "tra_oper",
    "unit",
    "geo",
    "time_period",
    "value",
    "flag"
FROM "eurostat-road-go-tq-tott"
