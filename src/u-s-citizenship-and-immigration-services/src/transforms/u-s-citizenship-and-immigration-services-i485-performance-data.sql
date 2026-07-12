-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table preserves the source workbook at cell level; consumers must interpret `row_index`, `column_label`, and surrounding cells before aggregating `value_text`.
SELECT
    "entity_id",
    "source_url",
    "source_file",
    "source_format",
    "source_period",
    "source_year",
    "sheet_name",
    "row_index",
    "column_index",
    "column_label",
    "value_text"
FROM "u-s-citizenship-and-immigration-services-i485-performance-data"
