-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city",
    "state",
    "2015_murders",
    "2016_murders",
    "change",
    "source",
    "as_of"
FROM "fivethirtyeight-murder-2016-murder-2016-prelim"
