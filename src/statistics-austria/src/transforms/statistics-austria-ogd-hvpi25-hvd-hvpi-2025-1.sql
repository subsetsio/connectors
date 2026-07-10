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
    "weight_in_reporting_month"
FROM "statistics-austria-ogd-hvpi25-hvd-hvpi-2025-1"
