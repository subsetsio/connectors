-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_licence",
    "number_of_licences_issued"
FROM "sg-data-d-b5dfc383eb8e97e940ac555a226d7196"
