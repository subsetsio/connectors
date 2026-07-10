-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "overnight",
    "week_1",
    "week_2",
    "month_1",
    "month_2",
    "month_3",
    "month_6",
    "month_9",
    "month_12",
    "more_1_year"
FROM "bank-negara-malaysia-interbank-swap"
