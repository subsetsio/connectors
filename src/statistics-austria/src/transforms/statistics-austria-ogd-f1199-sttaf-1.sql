-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "gender_2",
    "life_tables_14",
    "age_in_years_111",
    "life_expectancy",
    "mortality",
    "mortality_table",
    "table_mortality",
    "population_in_hospitals"
FROM "statistics-austria-ogd-f1199-sttaf-1"
