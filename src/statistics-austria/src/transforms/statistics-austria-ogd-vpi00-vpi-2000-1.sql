-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "indices",
    "index_figure_reporting_month_annual_average",
    "index_figure_previous_month",
    "index_figure_same_month_of_previous_year_previous_year_s_average",
    "percent_change_from_previous_month",
    "percent_change_from_same_month_of_previous_year_previous_year"
FROM "statistics-austria-ogd-vpi00-vpi-2000-1"
