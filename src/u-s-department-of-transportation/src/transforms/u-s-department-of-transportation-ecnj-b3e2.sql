-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "a_weighted_24_hour_laeq_dba",
    CAST("number_of_people_in_2016" AS BIGINT) AS number_of_people_in_2016,
    CAST("percent_of_total_population" AS DOUBLE) AS percent_of_total_population,
    CAST("number_of_people_in_2018" AS BIGINT) AS number_of_people_in_2018,
    CAST("percent_of_total_population_1" AS DOUBLE) AS percent_of_total_population_1,
    CAST("change_2016_to_2018" AS DOUBLE) AS change_2016_to_2018
FROM "u-s-department-of-transportation-ecnj-b3e2"
