-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "region",
    "r_d_personnel_headcount_by_main_location_of_the_enterprise",
    "r_d_personnel_headcount_by_rad_location_of_the_enterprise",
    "r_d_personnel_fte_by_main_location_of_the_enterprise",
    "r_d_personnel_fte_by_rad_location_of_the_enterprise",
    "intramural_r_d_expenditures_by_main_location_of_the_enterprise_in_thousand_euro",
    "intramural_r_d_expenditures_by_rad_location_of_the_enterprise_in_thousand_euro"
FROM "statistics-austria-ogd-1905fue-fue-b1905fue-1"
