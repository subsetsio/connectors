-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "employees_choice_of_days_off",
    "shift_swapping",
    "time_banking",
    "flexi_shift"
FROM "sg-data-d-2bb9f23e0403158ce5b768dd4ef3c9ab"
