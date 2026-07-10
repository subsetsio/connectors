-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "fb_nummer",
    "oenace_zuord"
FROM "statistics-austria-ogdext-hvd-fbnr-oenace-1"
