-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "employees_choice_of_days_off",
    "shift_swapping",
    "time_banking",
    "flexi_shift"
FROM "sg-data-d-28b00faef00a758980fb9768c75df59b"
