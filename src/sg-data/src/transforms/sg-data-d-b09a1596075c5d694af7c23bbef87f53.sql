-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "school_type",
    "teachers_pri"
FROM "sg-data-d-b09a1596075c5d694af7c23bbef87f53"
