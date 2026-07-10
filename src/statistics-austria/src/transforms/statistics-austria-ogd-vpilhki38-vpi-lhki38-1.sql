-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "indices",
    "index_number_month_year"
FROM "statistics-austria-ogd-vpilhki38-vpi-lhki38-1"
