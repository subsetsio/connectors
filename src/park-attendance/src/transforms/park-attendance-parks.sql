-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "park_id",
    "park_name",
    "company",
    "country",
    "continent",
    "latitude",
    "longitude",
    "timezone"
FROM "park-attendance-parks"
