-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "sea_level_rise",
    "number_of_daysyear_with_maximum_temperature_at_or_above_82f",
    "number_of_daysyear_with_maximum_temperature_at_or_above_90f",
    "number_of_daysyear_with_maximum_temperature_at_or_above_95f",
    "number_of_daysyear_with_minimum_temperature_at_or_above_80f",
    "number_of_heatwavesyear",
    "average_length_of_heat_waves_in_days",
    "number_of_daysyear_with_heat_index_at_or_above_85f",
    "number_of_daysyear_with_heat_index_at_or_above_95f",
    "cooling_degree_days",
    "number_of_daysyear_with_minimum_temperature_at_or_below_32f",
    "heating_degree_days",
    "number_of_daysyear_with_rainfall_exceeding_1_inch",
    "number_of_daysyear_with_rainfall_exceeding_2_inches",
    "number_of_daysyear_with_rainfall_exceeding_4_inches"
FROM "nyc-open-data-38ps-fnsg"
