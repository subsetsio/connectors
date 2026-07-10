-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "In general, how worried are you about earthquakes?" AS in_general_how_worried_are_you_about_earthquakes,
    "How worried are you about the Big One, a massive, catastrophic earthquake?" AS how_worried_are_you_about_the_big_one_a_massive_catastrophic_earthquake,
    "Do you think the ""Big One"" will occur in your lifetime?" AS do_you_think_the_big_one_will_occur_in_your_lifetime,
    "Have you ever experienced an earthquake?" AS have_you_ever_experienced_an_earthquake,
    "Have you or anyone in your household taken any precautions for an earthquake (packed an earthquake survival kit, prepared an evacuation plan, etc.)?" AS have_you_or_anyone_in_your_household_taken_any_precautions_for_an_earthquake_packed_an_earthquake_survival_kit_prepared_an_evacuation_plan_etc,
    "How familiar are you with the San Andreas Fault line?" AS how_familiar_are_you_with_the_san_andreas_fault_line,
    "How familiar are you with the Yellowstone Supervolcano?" AS how_familiar_are_you_with_the_yellowstone_supervolcano,
    "Age" AS age,
    "What is your gender?" AS what_is_your_gender,
    "How much total combined money did all members of your HOUSEHOLD earn last year?" AS how_much_total_combined_money_did_all_members_of_your_household_earn_last_year,
    "US Region" AS us_region
FROM "fivethirtyeight-san-andreas-earthquake-data"
