-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "earnings_and_working_time",
    "sex",
    "full_and_part_time_employment",
    "nace_2008_nace_rev_2",
    "arithmetic_mean",
    "c_1st_quartile",
    "c_2nd_quartile_median",
    "c_3rd_quartile",
    "number_of_employees"
FROM "statistics-austria-ogd-veste301-veste301-1"
