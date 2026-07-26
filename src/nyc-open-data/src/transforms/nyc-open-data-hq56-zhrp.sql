-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo_dist",
    "bldg_id",
    "admin_dist",
    "bldg_name",
    "bldg_enroll",
    "historical_bldg_cap",
    "historical_bldg_util",
    "org_id",
    "incl_class",
    "organization_name",
    "org_enroll",
    "org_historical_cap",
    "org_historical_util",
    "prek_cap",
    "no_of_cluster_spec_rms_reported",
    "no_of_cluster_rms_needed"
FROM "nyc-open-data-hq56-zhrp"
