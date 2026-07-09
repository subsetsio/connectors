-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Punctuality tables combine annual and monthly reporting periods; filter the period field before time-series aggregation.
SELECT
    "Run Date" AS run_date,
    "Reporting Period" AS reporting_period,
    "Reporting Airport" AS reporting_airport,
    "Origin Destination" AS origin_destination,
    "Number Flights Matched" AS number_flights_matched,
    "Actual Flights Unmatched" AS actual_flights_unmatched,
    "Number Flights Cancelled" AS number_flights_cancelled,
    "Flights more than 15 minutes early percent" AS flights_more_than_15_minutes_early_percent,
    "Flights 15 minutes early to 1 minute early percent" AS flights_15_minutes_early_to_1_minute_early_percent,
    "Flights 0 (zero) to 15 minutes late percent" AS flights_0_zero_to_15_minutes_late_percent,
    "Flights between 16 and 30 minutes late percent" AS flights_between_16_and_30_minutes_late_percent,
    "Flights between 31 and 60 minutes late percent" AS flights_between_31_and_60_minutes_late_percent,
    "Flights between 61 and 120 minutes late percent" AS flights_between_61_and_120_minutes_late_percent,
    "Flights between 121 and 180 minutes late percent" AS flights_between_121_and_180_minutes_late_percent,
    "Flights between 181 and 360 minutes late percent" AS flights_between_181_and_360_minutes_late_percent,
    "Flights more than 360 minutes late percent" AS flights_more_than_360_minutes_late_percent,
    "Flights Unmatched Percent" AS flights_unmatched_percent,
    "Flights Cancelled Percent" AS flights_cancelled_percent,
    "Average Delay Minutes" AS average_delay_minutes,
    "Previous Year Month Flights Matched" AS previous_year_month_flights_matched,
    "Previous Year month early to 15 mins late percent" AS previous_year_month_early_to_15_mins_late_percent,
    "Previous Year Month Average Delay" AS previous_year_month_average_delay,
    "release_period",
    "family"
FROM "civil-aviation-authority-punctuality-summary-analysis"
