-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_category",
    "no_of_participants"
FROM "sg-data-d-01ad15c4d10ca87328f6af80b2ffbe82"
