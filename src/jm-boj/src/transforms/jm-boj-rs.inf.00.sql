-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The workbook contains multiple inflation-target outturn panels; include `subtable` when grouping rows.
SELECT
    "date",
    "subtable",
    "series",
    "value",
    "frequency",
    "unit"
FROM "jm-boj-rs.inf.00"
