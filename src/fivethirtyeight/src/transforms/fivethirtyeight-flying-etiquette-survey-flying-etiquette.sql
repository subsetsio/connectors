-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RespondentID" AS respondentid,
    "How often do you travel by plane?" AS how_often_do_you_travel_by_plane,
    "Do you ever recline your seat when you fly?" AS do_you_ever_recline_your_seat_when_you_fly,
    "How tall are you?" AS how_tall_are_you,
    "Do you have any children under 18?" AS do_you_have_any_children_under_18,
    "In a row of three seats, who should get to use the two arm rests?" AS in_a_row_of_three_seats_who_should_get_to_use_the_two_arm_rests,
    "In a row of two seats, who should get to use the middle arm rest?" AS in_a_row_of_two_seats_who_should_get_to_use_the_middle_arm_rest,
    "Who should have control over the window shade?" AS who_should_have_control_over_the_window_shade,
    "Is itrude to move to an unsold seat on a plane?" AS is_itrude_to_move_to_an_unsold_seat_on_a_plane,
    "Generally speaking, is it rude to say more than a few words tothe stranger sitting next to you on a plane?" AS generally_speaking_is_it_rude_to_say_more_than_a_few_words_tothe_stranger_sitting_next_to_you_on_a_plane,
    "On a 6 hour flight from NYC to LA, how many times is it acceptable to get up if you're not in an aisle seat?" AS on_a_6_hour_flight_from_nyc_to_la_how_many_times_is_it_acceptable_to_get_up_if_you_re_not_in_an_aisle_seat,
    "Under normal circumstances, does a person who reclines their seat during a flight have any obligation to the person sitting behind them?" AS under_normal_circumstances_does_a_person_who_reclines_their_seat_during_a_flight_have_any_obligation_to_the_person_sitting_behind_them,
    "Is itrude to recline your seat on a plane?" AS is_itrude_to_recline_your_seat_on_a_plane,
    "Given the opportunity, would you eliminate the possibility of reclining seats on planes entirely?" AS given_the_opportunity_would_you_eliminate_the_possibility_of_reclining_seats_on_planes_entirely,
    "Is it rude to ask someone to switch seats with you in order to be closer to friends?" AS is_it_rude_to_ask_someone_to_switch_seats_with_you_in_order_to_be_closer_to_friends,
    "Is itrude to ask someone to switch seats with you in order to be closer to family?" AS is_itrude_to_ask_someone_to_switch_seats_with_you_in_order_to_be_closer_to_family,
    "Is it rude to wake a passenger up if you are trying to go to the bathroom?" AS is_it_rude_to_wake_a_passenger_up_if_you_are_trying_to_go_to_the_bathroom,
    "Is itrude to wake a passenger up if you are trying to walk around?" AS is_itrude_to_wake_a_passenger_up_if_you_are_trying_to_walk_around,
    "In general, is itrude to bring a baby on a plane?" AS in_general_is_itrude_to_bring_a_baby_on_a_plane,
    "In general, is it rude to knowingly bring unruly children on a plane?" AS in_general_is_it_rude_to_knowingly_bring_unruly_children_on_a_plane,
    "Have you ever used personal electronics during take off or landing in violation of a flight attendant's direction?" AS have_you_ever_used_personal_electronics_during_take_off_or_landing_in_violation_of_a_flight_attendant_s_direction,
    "Have you ever smoked a cigarette in an airplane bathroom when it was against the rules?" AS have_you_ever_smoked_a_cigarette_in_an_airplane_bathroom_when_it_was_against_the_rules,
    "Gender" AS gender,
    "Age" AS age,
    "Household Income" AS household_income,
    "Education" AS education,
    "Location (Census Region)" AS location_census_region
FROM "fivethirtyeight-flying-etiquette-survey-flying-etiquette"
