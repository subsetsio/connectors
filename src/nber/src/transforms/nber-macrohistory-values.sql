-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table combines annual, quarterly, and monthly series; filter or group by frequency before comparing observation periods.
-- caution: A small number of source series contain multiple values for the same series and observation date without a separate upstream subseries label; keep value in the row identity when de-duplicating.
SELECT
    "series_id",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value",
    "frequency",
    "chapter"
FROM "nber-macrohistory-values"
