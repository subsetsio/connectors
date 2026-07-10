-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ID" AS id,
    "Pollster" AS pollster,
    "Polls" AS polls,
    "Live Caller With Cellphones" AS live_caller_with_cellphones,
    "Internet" AS internet,
    "NCPP/AAPOR/Roper" AS ncpp_aapor_roper,
    "Polls_1" AS polls_1,
    "Simple Average Error" AS simple_average_error,
    "Races Called Correctly" AS races_called_correctly,
    "Advanced Plus-Minus" AS advanced_plus_minus,
    "Predictive Plus-Minus" AS predictive_plus_minus,
    "538 Grade" AS 538_grade,
    "Banned by 538" AS banned_by_538,
    "Mean-Reverted Bias" AS mean_reverted_bias
FROM "fivethirtyeight-pollster-ratings-2016-pollster-ratings"
