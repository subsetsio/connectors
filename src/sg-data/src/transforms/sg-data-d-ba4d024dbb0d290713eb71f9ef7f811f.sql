-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_ref",
    "course_title",
    "gender_male",
    "gender_female"
FROM "sg-data-d-ba4d024dbb0d290713eb71f9ef7f811f"
