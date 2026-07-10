-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SHOW" AS show,
    "SEASON" AS season,
    "CONTESTANT" AS contestant,
    "ELIMINATION-1" AS elimination_1,
    "ELIMINATION-2" AS elimination_2,
    "ELIMINATION-3" AS elimination_3,
    "ELIMINATION-4" AS elimination_4,
    "ELIMINATION-5" AS elimination_5,
    "ELIMINATION-6" AS elimination_6,
    "ELIMINATION-7" AS elimination_7,
    "ELIMINATION-8" AS elimination_8,
    "ELIMINATION-9" AS elimination_9,
    "ELIMINATION-10" AS elimination_10,
    "DATES-1" AS dates_1,
    "DATES-2" AS dates_2,
    "DATES-3" AS dates_3,
    "DATES-4" AS dates_4,
    "DATES-5" AS dates_5,
    "DATES-6" AS dates_6,
    "DATES-7" AS dates_7,
    "DATES-8" AS dates_8,
    "DATES-9" AS dates_9,
    "DATES-10" AS dates_10
FROM "fivethirtyeight-bachelorette-bachelorette"
