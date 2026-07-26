-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_no" AS no,
    "form_submission_date",
    "reported_property_addresses",
    "reported_borough",
    "reported_dob_bin_number",
    "reported_dob_permit_sequence",
    "reported_units",
    "reported_affordale_units",
    "reported_commencement_date",
    "reported_anticipated_completion_date",
    "reported_property_tax_block",
    "reported_property_tax_lots",
    "reported_affordability_option",
    "presumed_borough",
    "presumed_community_board",
    "presumed_council_district",
    "presumed_duplicate",
    "presumed_duplicate_weight",
    "presumed_building_units",
    "presumed_building_affordable_units",
    "presumed_lot",
    "postcode",
    "latitude",
    "longitude",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-pq4c-wbq4"
