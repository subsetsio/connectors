-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ntd_id",
    "reporter_name",
    "reportertypeshort",
    "mode_code",
    "service_type_code",
    "states_served",
    CAST("serve_own_ntdid_flag" AS BOOLEAN) AS serve_own_ntdid_flag,
    CAST("has_psgnr_elig_rqmt_flag" AS BOOLEAN) AS has_psgnr_elig_rqmt_flag,
    "minadvanceresreq",
    CAST("fare_amount" AS DOUBLE) AS fare_amount
FROM "u-s-department-of-transportation-i3pw-uwab"
