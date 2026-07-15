-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "sick_leave",
    "avg_days_per_absentee",
    "avg_days_per_employee"
FROM "sg-data-d-735578adc09f2d33e8ede963b8d8feb9"
