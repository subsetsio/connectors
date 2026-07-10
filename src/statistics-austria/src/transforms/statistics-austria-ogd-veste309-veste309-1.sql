-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "sex",
    "citizenship",
    "region_nuts2",
    "form_of_employment",
    "arithmetic_mean",
    "c_1st_quartile",
    "c_2nd_quartile_median",
    "c_3rd_quartile",
    "number_of_employees"
FROM "statistics-austria-ogd-veste309-veste309-1"
