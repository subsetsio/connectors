-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("berichtsjahr" AS BIGINT) AS berichtsjahr,
    "regionale_zuordnung",
    "schulstufe",
    "number_of_records_f_kla"
FROM "statistics-austria-ogd-klassen-klassen-1"
