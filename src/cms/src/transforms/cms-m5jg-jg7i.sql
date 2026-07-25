-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    CAST("Percent of patients who reported that their home health team gave care in a professional way" AS BIGINT) AS pct_pts_who_reported_that_their_home_hea_care_a_professional_way,
    CAST("Percent of patients who reported that their home health team communicated well with them" AS BIGINT) AS pct_pts_who_reported_that_their_home_team_communicated_well_them,
    CAST("Percent of patients who reported that their home health team discussed medicines, pain, and home safety with them" AS BIGINT) AS pct_pts_who_reported_that_their_home_healt_pain_home_safety_them,
    CAST("Percent of patients who gave their home health agency a rating of 9 or 10 on a scale from 0 (lowest) to 10 (highest)" AS BIGINT) AS pct_pts_who_gave_their_home_health_agency_a_0_lowest_10_highest,
    CAST("Percent of patients who reported YES, they would definitely recommend the home health agency to friends and family" AS BIGINT) AS pct_pts_who_reported_yes_they_would_health_agency_friends_family,
    CAST("Number of completed Surveys" AS BIGINT) AS number_of_completed_surveys,
    CAST("Survey response rate" AS BIGINT) AS survey_response_rate
FROM "cms-m5jg-jg7i"
