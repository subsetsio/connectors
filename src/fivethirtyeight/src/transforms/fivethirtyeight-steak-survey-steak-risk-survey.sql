-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RespondentID" AS respondentid,
    "Consider the following hypothetical situations: <br>In Lottery A, you have a 50% chance of success, with a payout of $100. <br>In Lottery B, you have a 90% chance of success, with a payout of $20. <br><br>Assuming you have $10 to bet, would you play Lottery A or Lottery B?" AS consider_the_following_hypothetical_situations_br_in_lottery_a_you_have_a_50_chance_of_success_with_a_payout_of_100_br_in_lottery_b_you_have_a_90_chance_of_success_with_a_payout_of_20_br_br_assuming_you_have_10_to_bet_would_you_play_lottery_a_or_lottery_b,
    "Do you ever smoke cigarettes?" AS do_you_ever_smoke_cigarettes,
    "Do you ever drink alcohol?" AS do_you_ever_drink_alcohol,
    "Do you ever gamble?" AS do_you_ever_gamble,
    "Have you ever been skydiving?" AS have_you_ever_been_skydiving,
    "Do you ever drive above the speed limit?" AS do_you_ever_drive_above_the_speed_limit,
    "Have you ever cheated on your significant other?" AS have_you_ever_cheated_on_your_significant_other,
    "Do you eat steak?" AS do_you_eat_steak,
    "How do you like your steak prepared?" AS how_do_you_like_your_steak_prepared,
    "Gender" AS gender,
    "Age" AS age,
    "Household Income" AS household_income,
    "Education" AS education,
    "Location (Census Region)" AS location_census_region
FROM "fivethirtyeight-steak-survey-steak-risk-survey"
