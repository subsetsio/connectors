-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Period" AS BIGINT) AS period,
    "Mothers_Age" AS mothers_age,
    CAST("Age_specific_birth_rate" AS DOUBLE) AS age_specific_birth_rate,
    CAST("Count" AS BIGINT) AS count,
    "Birth_Death" AS birth_death,
    "Region" AS region,
    "Births_Deaths_or_Natural_Increase" AS births_deaths_or_natural_increase,
    "Sex" AS sex,
    "Age" AS age
FROM "statsnz-births-and-deaths-year-ended-december-2021-csv"
