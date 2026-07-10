-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "mode_of_traffic",
    "tonnes",
    "c_1000_tonne_kilometres_domestic",
    "c_1000_tonne_kilometres_abroad"
FROM "statistics-austria-ogd-gvk-ware-2010-gvk-w10-1"
