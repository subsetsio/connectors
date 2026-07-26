-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "housenumber",
    "streetname",
    "borough",
    "cbno",
    "job_number",
    "workpermitnumber",
    "ahv_permit_number",
    "ahvpermitstatus",
    "variancetype",
    "reasonforvariance",
    "variance_start_datetime",
    "variance_end_datetime",
    "is_a_residence_within_200feet_of_the_site",
    "is_all_the_work_within_an_enclosed_building",
    "does_work_involve_full_or_partial_demolition",
    "does_any_of_the_work_involve_crane_use",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bbl",
    "nta"
FROM "nyc-open-data-g76y-dcqj"
