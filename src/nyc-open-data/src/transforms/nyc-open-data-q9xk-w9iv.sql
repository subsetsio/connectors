-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo_dist",
    "org_id",
    "organization_name",
    "bldg_id",
    "incl_class",
    "building_name",
    "enroll",
    "historical_capacity",
    "historical_utilization",
    "prek_cap",
    "no_of_cluster_spec_rms_reported",
    "no_of_cluster_rms_needed"
FROM "nyc-open-data-q9xk-w9iv"
