-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "sick_leave",
    "avg_days_per_absentee",
    "avg_days_per_employee"
FROM "sg-data-d-aabbf079b16af63eccf483c18984ac5e"
