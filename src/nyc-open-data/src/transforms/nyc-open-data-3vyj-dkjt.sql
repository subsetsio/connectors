-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_organization",
    "_program" AS program,
    "address",
    "borough",
    "postcode",
    "served_by",
    "event_date",
    "citywide_outreach",
    "age",
    "head_start_prek",
    "hospital_health_care",
    "seniors",
    "community_site",
    "hands_on",
    "special_needs",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-3vyj-dkjt"
