-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "column_1" AS codebook_identifier,
    "column_2" AS codebook_variable,
    "column_3" AS codebook_category,
    "column_4" AS codebook_explanation,
    "column_5" AS codebook_note_2,
    "CACode" AS cacode,
    "VaCode" AS vacode,
    "Estimate" AS estimate,
    "Sampling_errorR" AS sampling_errorr,
    "Flag" AS flag,
    "ASE" AS ase
FROM "statsnz-te-pa-harakeke-data-from-te-kupenga-2018-csv"
