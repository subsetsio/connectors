-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "type_of_summary",
    "summary",
    "native_american",
    "asian",
    "black",
    "hispaniclatinx",
    "white",
    "multiracial",
    "_unknown" AS unknown,
    "total"
FROM "nyc-open-data-unse-x4pq"
