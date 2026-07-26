-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "assigned_vendor",
    "org_testing_code",
    "dbn",
    "building_code",
    "_name" AS name,
    "building_primary_address_line_1",
    "building_borough",
    "building_zip",
    "grade_span",
    "geographic_district",
    "admin_district"
FROM "nyc-open-data-7a57-qgkz"
