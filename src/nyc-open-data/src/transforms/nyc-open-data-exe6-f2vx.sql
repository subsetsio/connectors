-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "community_school_district",
    "of_graduates",
    "of_graduates_that_completed_2_credits_in_arts",
    "of_graduates_that_completed_2_credits_in_arts_1",
    "of_8th_grade_students",
    "of_8th_grade_students_that_received_2_halfunits_of_instruction_in_arts",
    "of_8th_grade_students_that_received_2_halfunits_of_instruction_in_arts_1",
    "of_8th_grade_students_that_received_2_halfunits_of_instruction_in_arts_in_two_different_disciplines",
    "of_8th_grade_students_that_received_2_halfunits_of_instruction_in_arts_in_two_different_disciplines_1",
    "of_schools_serving_grades_15",
    "of_schools_serving_grades_15_that_provided_arts_instruction_in_all_four_disciplines_music_dance_theater_visual_arts",
    "of_schools_serving_grades_15_that_provided_arts_instruction_in_all_four_disciplines_music_dance_theater_visual_arts_1",
    "of_schools_serving_grade_6",
    "of_schools_serving_grade_6_that_provided_arts_instruction_in_all_four_disciplines_dance_music_theater_visual_arts",
    "of_schools_serving_grade_6_that_provided_arts_instruction_in_all_four_disciplines_dance_music_theater_visual_arts_1",
    "number_of_fulltime_teachers_certified_in_dance",
    "number_of_fulltime_teachers_certified_in_music",
    "number_of_fulltime_teachers_certified_in_theater",
    "number_of_fulltime_teachers_certified_in_visual_arts",
    "number_of_parttime_teachers_certified_in_dance",
    "number_of_parttime_teachers_certified_in_music",
    "number_of_parttime_teachers_certified_in_theater",
    "number_of_parttime_teachers_certified_in_visual_arts"
FROM "nyc-open-data-exe6-f2vx"
