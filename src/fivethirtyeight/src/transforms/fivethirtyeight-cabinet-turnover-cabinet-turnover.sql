-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "president",
    "position",
    "appointee",
    "start_date",
    "end_date",
    "length",
    "departure_day",
    "gender",
    "C8" AS c8,
    "_1" AS "1"
FROM "fivethirtyeight-cabinet-turnover-cabinet-turnover"
