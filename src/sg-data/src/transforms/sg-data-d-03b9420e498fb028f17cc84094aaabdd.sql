-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "media_activity",
    "sample_size",
    "mean_hours"
FROM "sg-data-d-03b9420e498fb028f17cc84094aaabdd"
