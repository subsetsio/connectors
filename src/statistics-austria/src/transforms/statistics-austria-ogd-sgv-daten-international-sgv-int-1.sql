-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "type_of_goods_nst_r_chapter",
    "time",
    "number_of_transport_units",
    "number_of_teus",
    "tonnes",
    "c_1000_tonne_kilometres_domestic"
FROM "statistics-austria-ogd-sgv-daten-international-sgv-int-1"
