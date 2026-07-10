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
    "COVID-19 HCP Measure Score" AS covid_19_hcp_measure_score,
    "COVID-19 HCP Reason for No Score (See Footnotes File)" AS covid_19_hcp_reason_for_no_score_see_footnotes_file,
    CAST("State Average COVID-19 HCP Measure Score" AS BIGINT) AS state_average_covid_19_hcp_measure_score,
    CAST("National Average COVID-19 HCP Measure Score" AS BIGINT) AS national_average_covid_19_hcp_measure_score
FROM "cms-covid-19-hcp"
