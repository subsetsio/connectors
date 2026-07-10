-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Rank" AS rank,
    "Pollster" AS pollster,
    "Pollster Rating ID" AS pollster_rating_id,
    "Polls Analyzed" AS polls_analyzed,
    "NCPP/AAPOR/Roper" AS ncpp_aapor_roper,
    "Banned by 538" AS banned_by_538,
    "Predictive Plus-Minus" AS predictive_plus_minus,
    "538 Grade" AS "538_grade",
    "Mean-Reverted Bias" AS mean_reverted_bias,
    "Races Called Correctly" AS races_called_correctly,
    "Misses Outside MOE" AS misses_outside_moe,
    "Simple Average Error" AS simple_average_error,
    "Simple Expected Error" AS simple_expected_error,
    "Simple Plus-Minus" AS simple_plus_minus,
    "Advanced Plus-Minus" AS advanced_plus_minus,
    "Mean-Reverted Advanced Plus Minus" AS mean_reverted_advanced_plus_minus,
    "# of Polls for Bias Analysis" AS of_polls_for_bias_analysis,
    "Bias" AS bias,
    "House Effect" AS house_effect,
    "Average Distance from Polling Average (ADPA)" AS average_distance_from_polling_average_adpa,
    "Herding Penalty" AS herding_penalty
FROM "fivethirtyeight-pollster-ratings-2021-pollster-ratings"
