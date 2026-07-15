-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Number_of_Employers_That_Support_Hiring_Exoffenders" AS number_of_employers_that_support_hiring_exoffenders,
    "Number_of_Inmates_Assisted" AS number_of_inmates_assisted,
    "Percentage_of_Assisted_Inmates_who_Secured_Jobs" AS percentage_of_assisted_inmates_who_secured_jobs
FROM "sg-data-d-736a79e272d44ff6663e0d8c28af5456"
