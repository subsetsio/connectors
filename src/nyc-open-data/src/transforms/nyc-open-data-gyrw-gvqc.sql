-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "encounter_timestamp",
    "park_area_id",
    "park_district",
    "park_borough",
    "patroncount",
    "in_playground",
    "action_taken",
    "amenity"
FROM "nyc-open-data-gyrw-gvqc"
