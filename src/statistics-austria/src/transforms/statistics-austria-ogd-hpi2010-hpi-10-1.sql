-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "hpi_total",
    "new_dwellings",
    "existing_dwellings",
    "existing_houses",
    "existing_flats"
FROM "statistics-austria-ogd-hpi2010-hpi-10-1"
