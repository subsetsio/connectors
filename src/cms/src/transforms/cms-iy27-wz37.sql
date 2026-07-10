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
    "HCAHPS Measure ID" AS hcahps_measure_id,
    "HCAHPS Question" AS hcahps_question,
    "HCAHPS Answer Description" AS hcahps_answer_description,
    "Patient Survey Star Rating" AS patient_survey_star_rating,
    "Patient Survey Star Rating Footnote" AS patient_survey_star_rating_footnote,
    "HCAHPS Answer Percent" AS hcahps_answer_percent,
    "HCAHPS Answer Percent Footnote" AS hcahps_answer_percent_footnote,
    "HCAHPS Linear Mean Value" AS hcahps_linear_mean_value,
    CAST("Number of Completed Surveys" AS BIGINT) AS number_of_completed_surveys,
    "Number of Completed Surveys Footnote" AS number_of_completed_surveys_footnote,
    CAST("Survey Response Rate Percent" AS BIGINT) AS survey_response_rate_percent,
    "Survey Response Rate Percent Footnote" AS survey_response_rate_percent_footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-iy27-wz37"
