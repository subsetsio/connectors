-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `series` values are local business firm size categories; distinguish category rows from totals before aggregating.
SELECT
    "date",
    "subtable",
    "series",
    "value",
    "frequency",
    "unit"
FROM "jm-boj-fs.dti.02"
