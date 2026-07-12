-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "column_1",
    "column_2",
    "column_3",
    "column_4",
    "column_5",
    "column_6",
    "CACode" AS cacode,
    "VaCode" AS vacode,
    "Count" AS count,
    "Percentage" AS percentage,
    "SCCode" AS sccode
FROM "statsnz-te-pa-harakeke-data-from-2018-census-csv"
