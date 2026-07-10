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
    "STrR Measure Score" AS strr_measure_score,
    "STrR Reason for No Score (See Footnotes File)" AS strr_reason_for_no_score_see_footnotes_file,
    CAST("State Average STrR Measure Score" AS BIGINT) AS state_average_strr_measure_score,
    CAST("National Average STrR Measure Score" AS BIGINT) AS national_average_strr_measure_score
FROM "cms-strr"
