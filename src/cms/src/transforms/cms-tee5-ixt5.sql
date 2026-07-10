-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    CAST("Quality of Patient Care Star Rating" AS DOUBLE) AS quality_of_patient_care_star_rating,
    CAST("Star Rating 1 Percentage" AS DOUBLE) AS star_rating_1_percentage,
    CAST("Star Rating 1.5 Percentage" AS DOUBLE) AS star_rating_1_5_percentage,
    CAST("Star Rating 2 Percentage" AS DOUBLE) AS star_rating_2_percentage,
    CAST("Star Rating 2.5 Percentage" AS DOUBLE) AS star_rating_2_5_percentage,
    CAST("Star Rating 3 Percentage" AS DOUBLE) AS star_rating_3_percentage,
    CAST("Star Rating 3.5 Percentage" AS DOUBLE) AS star_rating_3_5_percentage,
    CAST("Star Rating 4 Percentage" AS DOUBLE) AS star_rating_4_percentage,
    CAST("Star Rating 4.5 Percentage" AS DOUBLE) AS star_rating_4_5_percentage,
    CAST("Star Rating 5 Percentage" AS DOUBLE) AS star_rating_5_percentage,
    CAST("How often the home health team began their patients' care in a timely manner" AS DOUBLE) AS how_often_the_home_health_team_began_their_patients_care_in_a_timely_manner,
    CAST("How often the home health team determined whether patients received a flu shot for the current flu season" AS DOUBLE) AS how_often_the_home_health_team_determined_whether_patients_received_a_flu_shot_for_the_current_flu_season,
    CAST("How often patients got better at walking or moving around" AS DOUBLE) AS how_often_patients_got_better_at_walking_or_moving_around,
    CAST("How often patients got better at getting in and out of bed" AS DOUBLE) AS how_often_patients_got_better_at_getting_in_and_out_of_bed,
    CAST("How often patients got better at bathing" AS DOUBLE) AS how_often_patients_got_better_at_bathing,
    CAST("How often patients' breathing improved" AS DOUBLE) AS how_often_patients_breathing_improved,
    CAST("How often patients got better at taking their drugs correctly by mouth" AS DOUBLE) AS how_often_patients_got_better_at_taking_their_drugs_correctly_by_mouth,
    CAST("Changes in Skin Integrity post-acute care: pressure ulcer/injury" AS DOUBLE) AS changes_in_skin_integrity_post_acute_care_pressure_ulcer_injury,
    CAST("How often physician-recommended actions to address medication issues were completely timely" AS DOUBLE) AS how_often_physician_recommended_actions_to_address_medication_issues_were_completely_timely,
    CAST("Percent of Residents Experiencing One or More Falls with Major Injury" AS DOUBLE) AS percent_of_residents_experiencing_one_or_more_falls_with_major_injury,
    CAST("Discharge Function Score" AS DOUBLE) AS discharge_function_score,
    CAST("Transfer of Health Information to the Provider" AS DOUBLE) AS transfer_of_health_information_to_the_provider,
    CAST("Transfer of Health Information to the Patient" AS DOUBLE) AS transfer_of_health_information_to_the_patient,
    CAST("How much Medicare spends on an episode of care by agencies in this state, compared to Medicare spending across all agencies nationally" AS DOUBLE) AS how_much_medicare_spends_on_an_episode_of_care_by_agencies_in_this_state_compared_to_medicare_spending_across_all_agencies_nationally
FROM "cms-tee5-ixt5"
