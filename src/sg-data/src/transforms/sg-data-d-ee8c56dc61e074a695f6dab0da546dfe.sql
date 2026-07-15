-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "school_type",
    "students_preu"
FROM "sg-data-d-ee8c56dc61e074a695f6dab0da546dfe"
