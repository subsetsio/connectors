-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "period_of_survey",
    "indices",
    "index_figure_reporting_month_annual_average"
FROM "statistics-austria-ogd-vpi76-vpi-1976-1"
