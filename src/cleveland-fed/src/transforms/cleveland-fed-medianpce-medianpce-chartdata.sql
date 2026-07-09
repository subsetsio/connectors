-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A short chart window (the most recent years only) of series that exist in full elsewhere in this source; do not treat it as a complete history.
-- caution: All three columns are year-over-year percent changes.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "median_pce",
    "pce",
    "core_pce"
FROM "cleveland-fed-medianpce-medianpce-chartdata"
