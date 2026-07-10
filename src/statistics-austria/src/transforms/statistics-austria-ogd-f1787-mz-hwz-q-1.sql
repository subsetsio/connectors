-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "legal_basis_of_dwelling_6",
    "time_section",
    "number_of_dwellings_main_residence_in_1_000"
FROM "statistics-austria-ogd-f1787-mz-hwz-q-1"
