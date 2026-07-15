-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school_type",
    "number_of_sec_sch"
FROM "sg-data-d-041568b8e59c3cba17a178a68d4dcb7c"
