-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "geographical_district",
    "admin_district",
    "ats_code",
    "location_name",
    "grade_level",
    "building_code",
    "building_name",
    "address",
    "building_ownership_description",
    "room_no",
    "area",
    "_function" AS function,
    "is_school_colocated",
    "inside_v_outside",
    "is_the_space_shared_by_any_other_schools",
    "space_used_for_any_other_purpose_beside_pe"
FROM "nyc-open-data-xqmg-7z3j"
