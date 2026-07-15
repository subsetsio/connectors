-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_course",
    "type_of_study",
    "count"
FROM "sg-data-d-f1348b19dfd80e217b300977dffcc510"
