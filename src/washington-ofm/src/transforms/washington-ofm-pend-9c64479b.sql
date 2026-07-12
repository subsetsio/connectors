-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a faithful cell-level extract from an OFM file; use sheet_name, row_index, column_index, and value_text to reconstruct the source layout before aggregating values.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_source_url" AS source_url,
    "_source_file" AS source_file,
    "_source_member" AS source_member,
    "sheet_name",
    "row_index",
    "column_index",
    "value_text"
FROM "washington-ofm-pend-9c64479b"
