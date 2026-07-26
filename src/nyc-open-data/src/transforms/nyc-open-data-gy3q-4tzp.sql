-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dcid",
    "permit_number",
    "program_name",
    "facility_type",
    "program_type",
    "street_address",
    "borough",
    "zip_code",
    "phone_number",
    "child_age_range",
    "children_allowed_in_care",
    "administer_medication",
    "bin",
    "bbl",
    "community_board",
    "council_district",
    "census_tract",
    "nta_code",
    "latitude",
    "longitude"
FROM "nyc-open-data-gy3q-4tzp"
