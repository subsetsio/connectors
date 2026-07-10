-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "team_id",
    "team_name",
    "team_seed",
    "team_region",
    "playin_flag",
    "team_alive",
    "rd1_win",
    "rd2_win",
    "rd3_win",
    "rd4_win",
    "rd5_win",
    "rd6_win",
    "rd7_win",
    "win_odds"
FROM "fivethirtyeight-march-madness-predictions-bracket-00"
