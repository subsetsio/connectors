-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "opt_code",
    "_name" AS name,
    "affiliation",
    "site_type",
    "street_address",
    "city",
    "state",
    "zip",
    "longitude",
    "latitude",
    "door_to_door_service",
    "stop_to_school_service",
    "common_carrier_svc_metrocards",
    "site_reimbursement",
    "mid_day_service",
    "d2d_late_day_programs",
    "s2s_late_day_programs"
FROM "nyc-open-data-hg3c-2jsy"
