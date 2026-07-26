-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_no" AS no,
    "form_submission_date",
    "reported_property_address",
    "reported_property_borough",
    "reported_dob_bin_number",
    "reported_dob_permit_sequence",
    "reported_property_tax_block",
    "reported_property_tax_lot",
    "reported_units",
    "reported_restricted_units",
    "reported_commencement_date",
    "reported_anticipated_completion_date",
    "reported_affordability_option",
    "presumed_community_board",
    "presumed_duplicate",
    "duplicate_count",
    "presumed_building_units",
    "presumed_building_restricted_units",
    "presumed_bbl",
    "postcode",
    "latitude",
    "longitude",
    "council_district",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-rrtd-iyd7"
