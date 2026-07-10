-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows represent non-empty cells from formatted BCB bulletin spreadsheets; interpret row and column positions with the original table layout rather than summing cells as a normalized panel.
SELECT
    "table_code",
    "sheet",
    "row",
    "col",
    "value_num",
    "value_text"
FROM "banco-central-de-bolivia-02-13p"
