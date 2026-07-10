-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "cpa_gruppen_des_ghpi_2025",
    "ghpi_2025"
FROM "statistics-austria-ogd-pregpi004-ghpi-25-1"
