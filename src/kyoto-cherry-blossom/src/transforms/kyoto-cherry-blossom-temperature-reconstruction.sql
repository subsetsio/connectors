-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The reconstructed and observed March temperature columns cover different historical periods; use the appropriate column for the time span being analyzed.
SELECT
    "year",
    "temp_reconstructed",
    "temp_observed"
FROM "kyoto-cherry-blossom-temperature-reconstruction"
