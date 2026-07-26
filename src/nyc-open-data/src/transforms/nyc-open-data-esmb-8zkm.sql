-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "borough",
    "building_id",
    "org_id",
    "school",
    "project",
    "description",
    "fy",
    "total"
FROM "nyc-open-data-esmb-8zkm"
