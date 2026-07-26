-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough_location",
    "park_location",
    "sports_played",
    "week_start_date",
    "week_end_date",
    "sundays_attendance",
    "mondays_attendance",
    "tuesdays_attendance",
    "wednesdays_attendance",
    "thursdays_attendance",
    "fridays_attendance",
    "saturdays_attendance",
    "attendance_sum"
FROM "nyc-open-data-xeg4-ic28"
