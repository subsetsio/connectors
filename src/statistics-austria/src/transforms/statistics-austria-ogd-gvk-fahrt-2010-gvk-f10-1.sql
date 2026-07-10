-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "type_of_transport",
    "number_of_laden_journeys",
    "number_of_unladen_journeys"
FROM "statistics-austria-ogd-gvk-fahrt-2010-gvk-f10-1"
