-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Newspaper" AS newspaper,
    "Daily Circulation, 2004" AS daily_circulation_2004,
    "Daily Circulation, 2013" AS daily_circulation_2013,
    "Change in Daily Circulation, 2004-2013" AS change_in_daily_circulation_2004_2013,
    "Pulitzer Prize Winners and Finalists, 1990-2003" AS pulitzer_prize_winners_and_finalists_1990_2003,
    "Pulitzer Prize Winners and Finalists, 2004-2014" AS pulitzer_prize_winners_and_finalists_2004_2014,
    "Pulitzer Prize Winners and Finalists, 1990-2014" AS pulitzer_prize_winners_and_finalists_1990_2014
FROM "fivethirtyeight-pulitzer-pulitzer-circulation-data"
