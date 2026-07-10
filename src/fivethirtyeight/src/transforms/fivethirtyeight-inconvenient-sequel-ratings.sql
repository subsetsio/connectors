-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "timestamp",
    "respondents",
    "category",
    "link",
    "average",
    "mean",
    "median",
    "1_votes",
    "2_votes",
    "3_votes",
    "4_votes",
    "5_votes",
    "6_votes",
    "7_votes",
    "8_votes",
    "9_votes",
    "10_votes",
    "1_pct",
    "2_pct",
    "3_pct",
    "4_pct",
    "5_pct",
    "6_pct",
    "7_pct",
    "8_pct",
    "9_pct",
    "10_pct"
FROM "fivethirtyeight-inconvenient-sequel-ratings"
