-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The early part of the bloom-date series is sparse because observations before the modern period are reconstructed from historical records rather than continuous instrumental monitoring.
SELECT
    "year",
    "day_of_year",
    "thirty_year_average"
FROM "kyoto-cherry-blossom-bloom-dates"
