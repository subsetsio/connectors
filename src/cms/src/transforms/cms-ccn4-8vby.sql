-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "HHCAHPS Survey Summary Star Rating" AS hhcahps_survey_summary_star_rating,
    "HHCAHPS Survey Summary Star Rating Footnote" AS hhcahps_survey_summary_star_rating_footnote,
    "Star Rating for health team gave care in a professional way" AS star_rating_for_health_team_gave_care_in_a_professional_way,
    "Footnote for Star Rating for gave care in a professional way" AS footnote_for_star_rating_for_gave_care_in_a_professional_way,
    "Percent of patients who reported that their home health team gave care in a professional way" AS percent_of_patients_who_reported_that_their_home_health_team_gave_care_in_a_professional_way,
    "Footnote for Percent of patients who reported that their home health team gave care in a professional way" AS footnote_for_percent_of_patients_who_reported_that_their_home_health_team_gave_care_in_a_professional_way,
    "Star Rating for health team communicated well with them" AS star_rating_for_health_team_communicated_well_with_them,
    "Footnote for Star Rating for communicated well with them" AS footnote_for_star_rating_for_communicated_well_with_them,
    "Percent of patients who reported that their home health team communicated well with them" AS percent_of_patients_who_reported_that_their_home_health_team_communicated_well_with_them,
    "Footnote for Percent of patients who reported that their home health team communicated well with them" AS footnote_for_percent_of_patients_who_reported_that_their_home_health_team_communicated_well_with_them,
    "Star Rating team discussed medicines, pain, and home safety" AS star_rating_team_discussed_medicines_pain_and_home_safety,
    "Footnote Star Rating discussed medicines, pain, home safety" AS footnote_star_rating_discussed_medicines_pain_home_safety,
    "Percent of patients who reported that their home health team discussed medicines, pain, and home safety with them" AS percent_of_patients_who_reported_that_their_home_health_team_discussed_medicines_pain_and_home_safety_with_them,
    "Footnote for Percent of patients who reported that their home health team discussed medicines, pain, and home safety with them" AS footnote_for_percent_of_patients_who_reported_that_their_home_health_team_discussed_medicines_pain_and_home_safety_with_them,
    "Star Rating for how patients rated overall care from agency" AS star_rating_for_how_patients_rated_overall_care_from_agency,
    "Footnote for Star Rating for overall care from agency" AS footnote_for_star_rating_for_overall_care_from_agency,
    "Percent of patients who gave their home health agency a rating of 9 or 10 on a scale from 0 (lowest) to 10 (highest)" AS percent_of_patients_who_gave_their_home_health_agency_a_rating_of_9_or_10_on_a_scale_from_0_lowest_to_10_highest,
    "Footnote for Percent of patients who gave their home health agency a rating of 9 or 10 on a scale from 0(lowest) to 10(highest)" AS footnote_for_percent_of_patients_who_gave_their_home_health_agency_a_rating_of_9_or_10_on_a_scale_from_0_lowest_to_10_highest,
    "Percent of patients who reported YES, they would definitely recommend the home health agency to friends and family" AS percent_of_patients_who_reported_yes_they_would_definitely_recommend_the_home_health_agency_to_friends_and_family,
    "Footnote for Percent of patients who reported YES, they would definitely recommend the home health agency to friends and family" AS footnote_for_percent_of_patients_who_reported_yes_they_would_definitely_recommend_the_home_health_agency_to_friends_and_family,
    "Number of completed Surveys" AS number_of_completed_surveys,
    "Footnote for number of completed surveys" AS footnote_for_number_of_completed_surveys,
    "Survey response rate" AS survey_response_rate,
    "Footnote for Survey response rate" AS footnote_for_survey_response_rate,
    "Footnote Number" AS footnote_number
FROM "cms-ccn4-8vby"
