-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "nature_of_employment",
    "overtime_of_all_employees",
    "overtime_of_employees_who_worked_overtime"
FROM "sg-data-d-ab4bdf37338902a257748b1d90b487f9"
