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
    "column_6" AS codebook_note_3,
    "CACode" AS cacode,
    "VaCode" AS vacode,
    "Count" AS count,
    "Percentage" AS percentage,
    "SCCode" AS sccode
FROM "statsnz-te-pa-harakeke-data-from-2018-census-csv"
