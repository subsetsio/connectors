-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "academic_programme",
    "yearly_enrolment"
FROM "sg-data-d-e06e3afd67b720e9199702c2f44ad790"
