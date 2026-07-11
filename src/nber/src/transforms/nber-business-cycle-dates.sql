-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are complete business-cycle episodes; use the peak and trough dates to distinguish contraction timing from the following expansion timing.
SELECT
    strptime("peak", '%Y-%m-%d')::DATE AS peak,
    strptime("trough", '%Y-%m-%d')::DATE AS trough
FROM "nber-business-cycle-dates"
