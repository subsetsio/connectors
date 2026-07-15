-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level",
    "course",
    "sex",
    "enrolment_secondary"
FROM "sg-data-d-c60f4952deb240f91b4c966544271197"
