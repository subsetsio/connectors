-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "CACode" AS cacode,
    "VaCode" AS vacode,
    "Estimate" AS estimate,
    "Sampling_errorR" AS sampling_errorr,
    "Flag" AS flag,
    "ASE" AS ase,
    "sheet_name",
    "column_1",
    "column_2",
    "column_3",
    "column_4"
FROM "statsnz-te-kupenga-2018-whakamutunga-te-reo-maori"
