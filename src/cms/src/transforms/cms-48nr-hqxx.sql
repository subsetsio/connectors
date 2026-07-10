-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    "Address" AS address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    "Telephone Number" AS telephone_number,
    "Patients who reported that staff definitely gave care in a professional way and the facility was clean" AS patients_who_reported_that_staff_definitely_gave_care_in_a_professional_way_and_the_facility_was_clean,
    "Patients who reported that staff somewhat gave care in a professional way or the facility was somewhat clean" AS patients_who_reported_that_staff_somewhat_gave_care_in_a_professional_way_or_the_facility_was_somewhat_clean,
    "Patients who reported that staff did not give care in a professional way or the facility was not clean" AS patients_who_reported_that_staff_did_not_give_care_in_a_professional_way_or_the_facility_was_not_clean,
    "Facilities and staff linear mean score" AS facilities_and_staff_linear_mean_score,
    "Patients who reported that staff definitely communicated about what to expect during and after the procedure" AS patients_who_reported_that_staff_definitely_communicated_about_what_to_expect_during_and_after_the_procedure,
    "Patients who reported that staff somewhat communicated about what to expect during and after the procedure" AS patients_who_reported_that_staff_somewhat_communicated_about_what_to_expect_during_and_after_the_procedure,
    "Patients who reported that staff did not communicate about what to expect during and after the procedure" AS patients_who_reported_that_staff_did_not_communicate_about_what_to_expect_during_and_after_the_procedure,
    "Communication about your procedure linear mean score" AS communication_about_your_procedure_linear_mean_score,
    "Patients who gave the facility a rating of 9 or 10 on a scale from 0 (lowest) to 10 (highest)" AS patients_who_gave_the_facility_a_rating_of_9_or_10_on_a_scale_from_0_lowest_to_10_highest,
    "Patients who gave the facility a rating of 7 or 8 on a scale from 0 (lowest) to 10 (highest)" AS patients_who_gave_the_facility_a_rating_of_7_or_8_on_a_scale_from_0_lowest_to_10_highest,
    "Patients who gave the facility a rating of 0 to 6 on a scale from 0 (lowest) to 10 (highest)" AS patients_who_gave_the_facility_a_rating_of_0_to_6_on_a_scale_from_0_lowest_to_10_highest,
    "Patients' rating of the facility linear mean score" AS patients_rating_of_the_facility_linear_mean_score,
    "Patients who reported YES they would DEFINITELY recommend the facility to family or friends" AS patients_who_reported_yes_they_would_definitely_recommend_the_facility_to_family_or_friends,
    "Patients who reported PROBABLY YES they would recommend the facility to family or friends" AS patients_who_reported_probably_yes_they_would_recommend_the_facility_to_family_or_friends,
    "Patients who reported NO, they would not recommend the facility to family or friends" AS patients_who_reported_no_they_would_not_recommend_the_facility_to_family_or_friends,
    "Patients recommending the facility linear mean score" AS patients_recommending_the_facility_linear_mean_score,
    "Footnote" AS footnote,
    "Number of Sampled Patients" AS number_of_sampled_patients,
    "Number of Completed Surveys" AS number_of_completed_surveys,
    "Survey Response Rate Percent" AS survey_response_rate_percent,
    "Start Date" AS start_date,
    "End Date" AS end_date
FROM "cms-48nr-hqxx"
