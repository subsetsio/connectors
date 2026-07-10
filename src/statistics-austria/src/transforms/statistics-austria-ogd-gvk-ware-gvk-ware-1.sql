-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "type_of_transport",
    "number_of_transport_units",
    "tonnes",
    "c_1000_tonne_kilometres",
    "c_1000_tonne_kilometres_domestic",
    "c_1000_tonne_kilometres_abroad"
FROM "statistics-austria-ogd-gvk-ware-gvk-ware-1"
