-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "ethnic_group",
    "type_of_family_nucleus",
    "percentage"
FROM "sg-data-d-b553c9286f58ba96ef0ee1088743da52"
