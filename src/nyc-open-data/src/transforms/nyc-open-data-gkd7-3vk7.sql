-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geo_dist",
    "bldg_id",
    "bldg_name",
    "bldg_enroll",
    "target_bldg_cap",
    "target_bldg_util",
    "org_id",
    "incl_class",
    "organization_name",
    "org_enroll",
    "org_target_cap",
    "org_target_util",
    "prek_cap",
    "no_of_cluster_spec_rms_reported",
    "no_of_cluster_rms_needed",
    "data_as_of"
FROM "nyc-open-data-gkd7-3vk7"
