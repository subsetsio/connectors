-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "team",
    "group",
    "wspi",
    "wspi_offense",
    "wspi_defense",
    "group_first",
    "group_second",
    "group_third_advance",
    "group_third_no_advance",
    "group_fourth",
    "sixteen",
    "quarter",
    "semi",
    "final",
    "win"
FROM "fivethirtyeight-womens-world-cup-predictions-wwc-forecast-20150616-220036"
