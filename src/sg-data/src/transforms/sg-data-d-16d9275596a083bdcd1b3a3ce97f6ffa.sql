-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_type",
    "course_name"
FROM "sg-data-d-16d9275596a083bdcd1b3a3ce97f6ffa"
