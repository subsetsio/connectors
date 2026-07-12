-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a global Wikimedia media-request series, not scoped to individual wiki projects.
SELECT
    "media_type",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "requests"
FROM "wikipedia-mediarequests"
