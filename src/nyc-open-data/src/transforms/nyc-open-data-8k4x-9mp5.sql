-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "cy_payroll_num_201415_only",
    "pyrl_desc",
    "last_name_only_201415",
    "employee_full_name_from_2016",
    "parking_fringe",
    "automobile_fringe",
    "total"
FROM "nyc-open-data-8k4x-9mp5"
