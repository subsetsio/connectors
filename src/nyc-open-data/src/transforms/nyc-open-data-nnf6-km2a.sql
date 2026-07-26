-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_year",
    "project_title",
    "institution",
    "borough",
    "park_name",
    "location_within_park",
    "taxa_or_area_of_study"
FROM "nyc-open-data-nnf6-km2a"
