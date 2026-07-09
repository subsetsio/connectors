-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Series descriptions are the verified row identity in this release; use series_code with the values table, but do not assume it is unique in the raw series catalog without checking the release.
SELECT
    "series_code",
    "description",
    "release",
    "uri",
    "goals",
    "targets",
    "indicators"
FROM "united-nations-series"
