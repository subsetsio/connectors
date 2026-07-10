-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "date_of_month",
    "day_of_week",
    "births"
FROM "fivethirtyeight-births-us-births-1994-2003-cdc-nchs"
