-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "carpark",
    "category",
    "weekdays_rate_1",
    "weekdays_rate_2",
    "saturday_rate",
    "sunday_publicholiday_rate"
FROM "sg-data-d-9f6056bdb6b1dfba57f063593e4f34ae"
