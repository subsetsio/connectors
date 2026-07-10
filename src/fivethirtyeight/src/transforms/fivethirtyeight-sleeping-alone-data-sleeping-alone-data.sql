-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "StartDate" AS startdate,
    "EndDate" AS enddate,
    "Which of the following best describes your current relationship status?" AS which_of_the_following_best_describes_your_current_relationship_status,
    "How long have you been in your current relationship? If you are not currently in a relationship, please answer according to your last relationship." AS how_long_have_you_been_in_your_current_relationship_if_you_are_not_currently_in_a_relationship_please_answer_according_to_your_last_relationship,
    "When both you and your partner are at home, how often do you sleep in separate beds?" AS when_both_you_and_your_partner_are_at_home_how_often_do_you_sleep_in_separate_beds,
    "When you're not sleeping in the same bed as your partner, where do you typically sleep?" AS when_you_re_not_sleeping_in_the_same_bed_as_your_partner_where_do_you_typically_sleep,
    "C6" AS c6,
    "When you're not sleeping in the same bed, where does your partner typically sleep?" AS when_you_re_not_sleeping_in_the_same_bed_where_does_your_partner_typically_sleep,
    "_1" AS "1",
    "What are the reasons that you sleep in separate beds? Please select all that apply." AS what_are_the_reasons_that_you_sleep_in_separate_beds_please_select_all_that_apply,
    "_2" AS "2",
    "_3" AS "3",
    "_4" AS "4",
    "_5" AS "5",
    "_6" AS "6",
    "_7" AS "7",
    "_8" AS "8",
    "_9" AS "9",
    "_10" AS "10",
    "_11" AS "11",
    "When was the first time you slept in separate beds?" AS when_was_the_first_time_you_slept_in_separate_beds,
    "To what extent do you agree with the following statement: ""sleeping in separate beds helps us to stay together.""" AS to_what_extent_do_you_agree_with_the_following_statement_sleeping_in_separate_beds_helps_us_to_stay_together,
    "To what extent do you agree with the following statement: ""we sleep better when we sleep in separate beds.""" AS to_what_extent_do_you_agree_with_the_following_statement_we_sleep_better_when_we_sleep_in_separate_beds,
    "To what extent do you agree with the following statement:ë_""our sex life has improved as a result of sleeping in separate beds.""ë_" AS to_what_extent_do_you_agree_with_the_following_statement_our_sex_life_has_improved_as_a_result_of_sleeping_in_separate_beds,
    "Which of the following best describes your current occupation?" AS which_of_the_following_best_describes_your_current_occupation,
    "_12" AS "12",
    "Gender" AS gender,
    "Age" AS age,
    "Household Income" AS household_income,
    "Education" AS education,
    "Location (Census Region)" AS location_census_region
FROM "fivethirtyeight-sleeping-alone-data-sleeping-alone-data"
