-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boro",
    "csd",
    "city_council_district",
    "bldg_id",
    "bldg_name",
    "org_id",
    "org_name",
    "room_category",
    "shared",
    "of_rooms"
FROM "nyc-open-data-ix3t-6s7r"
