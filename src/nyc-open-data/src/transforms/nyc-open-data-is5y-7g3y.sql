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
    "bldg_id",
    "bldg_name",
    "address",
    "ownership",
    "room_number",
    "sq_ft",
    "room_function",
    "shared_with_other_schools",
    "inside_v_outside",
    "space_used_for_any_other_purpose_beside_pe"
FROM "nyc-open-data-is5y-7g3y"
