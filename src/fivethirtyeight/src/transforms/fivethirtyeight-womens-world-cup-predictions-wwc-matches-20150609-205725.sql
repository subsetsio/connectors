-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "group",
    "team1",
    "team2",
    "team1_win",
    "team2_win",
    "tie"
FROM "fivethirtyeight-womens-world-cup-predictions-wwc-matches-20150609-205725"
