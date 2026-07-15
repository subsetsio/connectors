-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "gender",
    "mean",
    "standard_error_of_mean",
    "5th_percentile",
    "10th_percentile",
    "25th_percentile",
    "50th_percentile",
    "75th_percentile",
    "90th_percentile",
    "95th_percentile"
FROM "sg-data-d-6a42359b27477f8f6609855d2fbe04db"
