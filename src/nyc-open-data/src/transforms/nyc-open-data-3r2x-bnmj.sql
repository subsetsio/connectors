-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "programinitiative",
    "_year" AS year,
    "title",
    "artist",
    "partner",
    "site_location",
    "borough",
    "site_type",
    "project_type",
    "latitude",
    "longitude",
    "installation",
    "removal"
FROM "nyc-open-data-3r2x-bnmj"
