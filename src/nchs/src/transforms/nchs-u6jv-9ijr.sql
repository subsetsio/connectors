-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "jurisdiction",
    strptime("week_ending_date", '%m/%d/%Y')::DATE AS week_ending_date,
    "state_abbreviation",
    "year",
    "week",
    "cause_group",
    "number_of_deaths",
    "cause_subgroup",
    "time_period",
    "suppress",
    "note",
    "average_number_of_deaths_in_time_period",
    "difference_from_2015_2019_to_2020",
    "percent_difference_from_2015_2019_to_2020",
    "type"
FROM "nchs-u6jv-9ijr"
