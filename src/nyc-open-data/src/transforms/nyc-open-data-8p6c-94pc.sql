-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "park_or_playground",
    "week_start_date",
    "week_end_date",
    "sundays_attendance",
    "mondays_attendance",
    "tuesdays_attendance",
    "wednesdays_attendance",
    "thursdays_attendance",
    "fridays_attendance",
    "saturdays_attendance",
    "total_attendance"
FROM "nyc-open-data-8p6c-94pc"
