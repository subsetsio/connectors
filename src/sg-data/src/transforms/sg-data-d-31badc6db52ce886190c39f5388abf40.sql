-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "tax_type",
    "return_type",
    "no_of_returns"
FROM "sg-data-d-31badc6db52ce886190c39f5388abf40"
