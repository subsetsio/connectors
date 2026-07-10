-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "coicop_5_digit_code",
    "index_figure_reporting_month_annual_average",
    "index_figure_previous_month",
    "index_figure_same_month_of_previous_year_previous_year_s_average",
    "percent_change_from_previous_month",
    "percent_change_from_same_month_of_previous_year_previous_year",
    "contribution_compared_with_previous_month",
    "contribution_compared_with_same_month_of_previous_year_previous_year",
    "weight_in_reporting_month"
FROM "statistics-austria-ogd-vpi25c18-vpi-2025coicop18-1"
