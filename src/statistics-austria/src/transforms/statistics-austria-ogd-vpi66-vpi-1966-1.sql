-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "indices",
    "index_figure_reporting_month_annual_average"
FROM "statistics-austria-ogd-vpi66-vpi-1966-1"
