-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "case_number",
    "type_of_intake"
FROM "sg-data-d-9439ea87f910688c8218c361df531365"
