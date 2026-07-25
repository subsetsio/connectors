-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a long-form melt of multiple heterogeneous source files; filter by source_file and source_column before interpreting or aggregating value.
SELECT
    "source_file",
    "row_index",
    "column" AS "source_column",
    "value"
FROM "nhs-digital-national-diabetes-audit-report-1-care-processes-and-treatment-targets-2016-17"
