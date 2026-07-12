-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table preserves annual CSV files at cell level; each source row spans multiple cells, so consumers should pivot by `row_index` and `column_label` before employer-level analysis.
SELECT
    "entity_id",
    "source_url",
    "source_file",
    "source_format",
    CAST("source_period" AS BIGINT) AS source_period,
    "source_year",
    "sheet_name",
    "row_index",
    "column_index",
    "column_label",
    "value_text"
FROM "u-s-citizenship-and-immigration-services-h2a-employer-data-hub"
