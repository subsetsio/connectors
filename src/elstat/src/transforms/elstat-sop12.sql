-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one numeric workbook cell. Periods, classifications, units, geography, and other dimensions are preserved in row_label and col_label as source text, so filter and aggregate only after interpreting those labels for the specific publication.
SELECT
    "source_file",
    "sheet",
    "row_label",
    "col_label",
    "row_idx",
    "col_idx",
    "value"
FROM "elstat-sop12"
