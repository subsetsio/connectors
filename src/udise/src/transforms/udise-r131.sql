-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "nsqf_other",
    "govt_sec_hsec_schools",
    "location_name",
    "all_mgt_sec_hsec_schools",
    "all_mgt_nsqf",
    "nsqf_govt",
    "other_sec_hsec_schools",
    "nsqf_govtaided",
    "private_sec_hsec_schools",
    "govtaided_sec_hsec_schools",
    "nsqf_private"
FROM "udise-r131"
