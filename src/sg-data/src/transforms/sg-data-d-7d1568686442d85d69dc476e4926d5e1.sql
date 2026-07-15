-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_level",
    "participant_category",
    "fee_per_term"
FROM "sg-data-d-7d1568686442d85d69dc476e4926d5e1"
