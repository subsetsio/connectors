-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Punctuality tables combine annual and monthly reporting periods; filter the period field before time-series aggregation.
SELECT
    "run_date",
    "reporting_period",
    "reporting_airport",
    "origin_destination_country",
    "origin_destination",
    "airline_name",
    "scheduled_charter",
    "number_flights_matched",
    "actual_flights_unmatched",
    "number_flights_cancelled",
    "flights_more_than_15_minutes_early_percent",
    "flights_15_minutes_early_to_1_minute_early_percent",
    "flights_0_to_15_minutes_late_percent",
    "flights_between_16_and_30_minutes_late_percent",
    "flights_between_31_and_60_minutes_late_percent",
    "flights_between_61_and_120_minutes_late_percent",
    "flights_between_121_and_180_minutes_late_percent",
    "flights_between_181_and_360_minutes_late_percent",
    "flights_more_than_360_minutes_late_percent",
    "flights_unmatched_percent",
    "flights_cancelled_percent",
    "average_delay_mins",
    "previous_year_month_flights_matched",
    "previous_year_month_early_to_15_mins_late_percent",
    "previous_year_month_average_delay",
    "release_period",
    "family"
FROM "civil-aviation-authority-punctuality-full-analysis"
