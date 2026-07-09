-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Both series are ten-year yields in percent per year: `tips_yield` is the observed market TIPS yield, `model_yield` the model-implied real yield. The horizon is not encoded in the data.
-- caution: The model series is re-estimated over the whole history when the model is refit, so past values can change between runs.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "tips_yield",
    "model_yield"
FROM "cleveland-fed-inflationexpectations-inflationexpectations-chart2"
