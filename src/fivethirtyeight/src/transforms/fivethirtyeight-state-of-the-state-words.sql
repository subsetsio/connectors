-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "phrase",
    "category",
    "d_speeches",
    "r_speeches",
    "total",
    "percent_of_d_speeches",
    "percent_of_r_speeches",
    "chi2",
    "pval"
FROM "fivethirtyeight-state-of-the-state-words"
