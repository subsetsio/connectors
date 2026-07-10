-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Country" AS country,
    CAST("Percent of patients who reported that their home health team gave care in a professional way" AS BIGINT) AS percent_of_patients_who_reported_that_their_home_health_team_gave_care_in_a_professional_way,
    CAST("Percent of patients who reported that their home health team communicated well with them" AS BIGINT) AS percent_of_patients_who_reported_that_their_home_health_team_communicated_well_with_them,
    CAST("Percent of patients who reported that their home health team discussed medicines, pain, and home safety with them" AS BIGINT) AS percent_of_patients_who_reported_that_their_home_health_team_discussed_medicines_pain_and_home_safety_with_them,
    CAST("Percent of patients who gave their home health agency a rating of 9 or 10 on a scale from 0 (lowest) to 10 (highest)" AS BIGINT) AS percent_of_patients_who_gave_their_home_health_agency_a_rating_of_9_or_10_on_a_scale_from_0_lowest_to_10_highest,
    CAST("Percent of patients who reported YES, they would definitely recommend the home health agency to friends and family" AS BIGINT) AS percent_of_patients_who_reported_yes_they_would_definitely_recommend_the_home_health_agency_to_friends_and_family,
    CAST("Number of completed Surveys" AS BIGINT) AS number_of_completed_surveys,
    CAST("Survey response rate" AS BIGINT) AS survey_response_rate
FROM "cms-vxub-6swi"
