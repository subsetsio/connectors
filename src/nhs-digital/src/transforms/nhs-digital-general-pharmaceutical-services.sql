-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a long-form melt of heterogeneous source files and workbook sheets; filter by source_file and column before interpreting or aggregating value.
SELECT
    "source_file",
    "row_index",
    "column",
    "value"
FROM "nhs-digital-general-pharmaceutical-services"
