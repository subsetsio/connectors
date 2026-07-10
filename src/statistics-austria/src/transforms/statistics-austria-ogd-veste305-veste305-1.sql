-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "sex",
    "highest_completed_level_of_education",
    "age_groups",
    "length_of_service_in_the_enterprise",
    "occupational_groups_isco_08",
    "arithmetic_mean",
    "c_1st_quartile",
    "c_2nd_quartile_median",
    "c_3rd_quartile",
    "number_of_employees"
FROM "statistics-austria-ogd-veste305-veste305-1"
