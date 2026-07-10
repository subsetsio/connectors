-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pollster" AS pollster,
    "# of Polls" AS of_polls,
    "NCPP / AAPOR / Roper" AS ncpp_aapor_roper,
    "Exclusively Live Caller With Cellphones" AS exclusively_live_caller_with_cellphones,
    "Methodology" AS methodology,
    "Banned by 538" AS banned_by_538,
    "Historical Advanced Plus-Minus" AS historical_advanced_plus_minus,
    "Predictive    Plus-Minus" AS predictive_plus_minus,
    "538 Grade" AS 538_grade,
    "Mean-Reverted Bias" AS mean_reverted_bias,
    "Races Called Correctly" AS races_called_correctly,
    "Misses Outside MOE" AS misses_outside_moe,
    "Simple Average Error" AS simple_average_error,
    "Simple Expected Error" AS simple_expected_error,
    "Simple Plus-Minus" AS simple_plus_minus,
    "Advanced Plus-Minus" AS advanced_plus_minus,
    "Mean-Reverted Advanced Plus Minus" AS mean_reverted_advanced_plus_minus,
    "Predictive Plus-Minus" AS predictive_plus_minus_2,
    "# of Polls for Bias Analysis" AS of_polls_for_bias_analysis,
    "Bias" AS bias,
    "Mean-Reverted Bias_1" AS mean_reverted_bias_1,
    "House Effect" AS house_effect
FROM "fivethirtyeight-pollster-ratings-2018-pollster-ratings"
