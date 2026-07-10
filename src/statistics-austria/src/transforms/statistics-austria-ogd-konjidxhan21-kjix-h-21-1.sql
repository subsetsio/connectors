-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "reporting_period",
    "nace_trade",
    "turnover_index_nominal",
    "turnover_index_real",
    "index_of_persons_employed",
    "turnover_index_nominal_working_day_adjusted",
    "turnover_index_nominal_seasonally_adjusted",
    "turnover_index_real_working_day_adjusted",
    "turnover_index_real_seasonally_adjusted",
    "index_of_gross_wages_and_salaries",
    "index_of_gross_wages_and_salaries_working_day_adjusted",
    "index_of_hours_worked",
    "index_of_hours_worked_working_day_adjusted"
FROM "statistics-austria-ogd-konjidxhan21-kjix-h-21-1"
