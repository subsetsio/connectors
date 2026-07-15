-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_employee",
    "sick_leave",
    "avg_days_per_absentee",
    "avg_days_per_employee"
FROM "sg-data-d-0a10542a8c342d57b3b1cd824c436511"
