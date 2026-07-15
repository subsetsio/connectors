-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "overtime_of_all_employees",
    "overtime_of_employees_who_worked_overtime"
FROM "sg-data-d-f77122d6dae6b2a363d88fca166e53f4"
