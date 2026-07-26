-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "original_bbl",
    "_2021_bbl" AS 2021_bbl,
    "facility_type",
    "environmental_concern",
    "facility_feature",
    "map_year",
    "created_date",
    "image_id",
    "comments_string"
FROM "nyc-open-data-r9ca-6t4q"
