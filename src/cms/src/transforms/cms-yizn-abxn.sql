-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    "Address" AS address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    "Telephone Number" AS telephone_number,
    "OAS CAHPS Measure ID" AS oas_cahps_measure_id,
    "OAS CAHPS Question" AS oas_cahps_question,
    "OAS CAHPS Answer Description" AS oas_cahps_answer_description,
    "OAS CAHPS Answer Percent" AS oas_cahps_answer_percent,
    "OAS CAHPS Answer Percent Footnote" AS oas_cahps_answer_percent_footnote,
    "OAS CAHPS Linear Mean Value" AS oas_cahps_linear_mean_value,
    "Number of Completed Surveys" AS number_of_completed_surveys,
    "Number of Completed Surveys Footnote" AS number_of_completed_surveys_footnote,
    "Survey Response Rate Percent" AS survey_response_rate_percent,
    "Survey Response Rate Percent Footnote" AS survey_response_rate_percent_footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-yizn-abxn"
