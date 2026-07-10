-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility Name" AS facility_name,
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Alternate CCN" AS alternate_ccn,
    "Address" AS address,
    "City" AS city,
    "State" AS state,
    "Zip Code" AS zip_code,
    "Network" AS network,
    "Measure Name" AS measure_name,
    "Achievement Measure Ratio" AS achievement_measure_ratio,
    "NHSN BSI Measure Score" AS nhsn_bsi_measure_score,
    "NHSN BSI Reason for No Score (See Footnotes File)" AS nhsn_bsi_reason_for_no_score_see_footnotes_file,
    CAST("State Average NHSN BSI Measure Score" AS BIGINT) AS state_average_nhsn_bsi_measure_score,
    CAST("National Average NHSN BSI Measure Score" AS BIGINT) AS national_average_nhsn_bsi_measure_score
FROM "cms-nhsn-bsi"
