-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RespondentID" AS respondentid,
    "Do you typically check a daily weather report?" AS do_you_typically_check_a_daily_weather_report,
    "How do you typically check the weather?" AS how_do_you_typically_check_the_weather,
    "A specific website or app (please provide the answer)" AS a_specific_website_or_app_please_provide_the_answer,
    "If you had a smartwatch (like the soon to be released Apple Watch), how likely or unlikely would you be to check the weather on that device?" AS if_you_had_a_smartwatch_like_the_soon_to_be_released_apple_watch_how_likely_or_unlikely_would_you_be_to_check_the_weather_on_that_device,
    "Age" AS age,
    "What is your gender?" AS what_is_your_gender,
    "How much total combined money did all members of your HOUSEHOLD earn last year?" AS how_much_total_combined_money_did_all_members_of_your_household_earn_last_year,
    "US Region" AS us_region
FROM "fivethirtyeight-weather-check-weather-check"
