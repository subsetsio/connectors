-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Period" AS DOUBLE) AS period,
    "Inst_sector" AS inst_sector,
    CAST("Inst_sector_code" AS BIGINT) AS inst_sector_code,
    "Descriptor" AS descriptor,
    "SNA08TRANS" AS sna08trans,
    "Asset_liability_code" AS asset_liability_code,
    "Values" AS values
FROM "statsnz-accumulation-accounts-2008-2023-provisional"
