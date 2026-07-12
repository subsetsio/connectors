-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "gender_ar",
    "municipality",
    "municipality_ar",
    "value",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-beneficiaries-of-security-by-location-of-branch"
