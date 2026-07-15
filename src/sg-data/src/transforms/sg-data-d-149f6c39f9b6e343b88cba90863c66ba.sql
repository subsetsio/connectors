-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_employee",
    "work_week_pattern",
    "distribution"
FROM "sg-data-d-149f6c39f9b6e343b88cba90863c66ba"
