-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "cpa_gruppen_des_ghpi_2020",
    "ghpi_2020"
FROM "statistics-austria-ogd-pregpi003-ghpi-20-1"
