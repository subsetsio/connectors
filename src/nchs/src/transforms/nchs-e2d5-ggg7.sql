-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "jurisdiction",
    "group",
    "subgroup",
    "year_of_death",
    "month_of_death",
    "time_period",
    strptime("month_ending_date", '%m/%d/%Y')::DATE AS month_ending_date,
    "maternal_deaths",
    "live_births",
    "maternal_mortality_rate",
    "footnote"
FROM "nchs-e2d5-ggg7"
