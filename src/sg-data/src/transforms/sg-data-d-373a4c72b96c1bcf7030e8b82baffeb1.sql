-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_employee",
    "sick_leave",
    "proportion"
FROM "sg-data-d-373a4c72b96c1bcf7030e8b82baffeb1"
