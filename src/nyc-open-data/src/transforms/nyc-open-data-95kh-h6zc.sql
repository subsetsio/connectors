-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dewatering_facility_name",
    "dewatering_facility_location",
    "_year" AS year,
    "dewatered_solidsbiosolids_allocation_dry_metric_tons",
    "management_practice_site_location",
    "management_practice_type",
    "management_practice_detail",
    "applicationdisposal_location",
    "pathogen_reduction_option",
    "vector_attraction_reduction_option",
    "biosolids_class_type"
FROM "nyc-open-data-95kh-h6zc"
