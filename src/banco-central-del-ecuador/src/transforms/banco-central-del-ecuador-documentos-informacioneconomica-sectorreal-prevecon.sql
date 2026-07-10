-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are extracted cells from formatted multi-sheet BCE Excel workbooks; sheet, row, and column context must be used before aggregating numeric values because workbooks can include headers, totals, subtotals, notes, and mixed table layouts.
SELECT
    "sheet",
    "row_index",
    "col_index",
    "row_label",
    "col_header",
    "value",
    "value_text"
FROM "banco-central-del-ecuador-documentos-informacioneconomica-sectorreal-prevecon"
